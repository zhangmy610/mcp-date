import asyncio
import requests
import logging
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置日志记录，设置日志级别为 INFO，即记录信息性消息
logging.basicConfig(level=logging.INFO)

# 模型服务的 URL，根据你提供的信息修改
MODEL_SERVICE_URL = 'http://localhost:5670/api/v1/chat/completions'

# 工具描述，定义了三个工具及其功能描述
tool_descriptions = {
    "query_table": "用于执行 SQL 查询语句，返回查询结果",
    "query_explain": "用于查询 SQL 语句的执行计划",
    "get_table_creation_statement": "用于返回指定表的创建语句"
}

# 定义 MCPClient 类，用于与服务器建立连接并处理查询
class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        # 初始化会话对象，初始值为 None
        self.session: Optional[ClientSession] = None
        # 创建一个 AsyncExitStack 对象，用于管理异步上下文
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        # 判断服务器脚本文件是否为 Python 文件
        is_python = server_script_path.endswith('.py')
        # 判断服务器脚本文件是否为 JavaScript 文件
        is_js = server_script_path.endswith('.js')
        # 如果文件既不是 Python 文件也不是 JavaScript 文件，则抛出异常
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        # 根据文件类型选择执行命令
        command = "python" if is_python else "node"
        # 创建 StdioServerParameters 对象，用于配置服务器参数
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        # 进入异步上下文，启动 stdio 客户端
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        # 从传输对象中获取 stdio 和 write 对象
        self.stdio, self.write = stdio_transport
        # 进入异步上下文，创建客户端会话
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        # 初始化会话
        await self.session.initialize()

        # List available tools
        # 列出服务器上可用的工具
        response = await self.session.list_tools()
        # 获取工具列表
        tools = response.tools
        # 记录日志，显示已连接到服务器以及可用的工具
        logging.info(f"Connected to server with tools: {[tool.name for tool in tools]}")

    async def process_query(self, query: str) -> str:
        """Process a query using the model service and available tools"""
        # 构建发送给模型的提示信息，包含用户问题和工具描述
        prompt = f"用户问题: {query}\n工具描述: {tool_descriptions}\n请选择合适的工具及参数（格式: 工具名称|参数）"

        # 构建请求数据，包含提示信息、模型名称等
        request_data = {
            "conv_uid": "",
            "request_message_id": "",
            "parent_id": "0",
            "user_input": prompt,
            "user_name": "",
            "chat_mode": "chat_normal",
            "select_param": "",
            "model_name": "deepseek_proxyllm",
            "stream": False
        }

        # 向模型服务发送请求
        try:
            # 发送 POST 请求到模型服务的 URL
            response = requests.post(MODEL_SERVICE_URL, json=request_data)
            # 手动指定编码为 UTF-8
            response.encoding = 'utf-8'
            # 如果请求成功（状态码为 200）
            if response.status_code == 200:
                try:
                    # 将响应内容解析为 JSON 格式
                    response_json = response.json()
                    # 从 JSON 数据中提取答案
                    answer = response_json.get('choices', [{}])[0].get('delta', {}).get('content', '')
                    # 尝试从回答中提取多个工具信息
                    import re
                    # 优化正则表达式，匹配包含已知工具名的行
                    tool_names = '|'.join(tool_descriptions.keys())
                    pattern = re.compile(rf'^\s*({tool_names})\|([^|]+)$', re.M)
                    # 使用正则表达式搜索答案
                    matches = pattern.findall(answer)
                    results = []
                    for match in matches:
                        # 提取工具名称
                        tool_name = match[0]
                        # 提取参数并去除多余字符
                        param_str = match[1].strip()
                        param_str = param_str.replace('```', '').strip()
                        # 将参数转换为工具要求的格式
                        if tool_name in tool_names:
                            params = {"query": param_str}
                        else:
                            params = {"arguments": param_str}
                        # 记录提取到的工具名和参数
                        logging.info(f"提取到的工具名: {tool_name}")
                        logging.info(f"提取到的参数: {params}")
                        # 调用 MCP 工具
                        result = await self.session.call_tool(tool_name, params)
                        results.append(f"[Calling tool {tool_name} with args {params}]\n{result.content}")
                    return '\n'.join(results)
                except ValueError as e:
                    # 如果解析 JSON 失败，返回错误信息
                    return f"无法将响应解析为 JSON 格式，详细错误信息: {e}"
            else:
                # 如果请求失败，返回错误信息
                return f"请求模型服务失败，状态码: {response.status_code}"
        except requests.RequestException as e:
            # 如果发生网络错误，返回错误信息
            return f"请求模型服务时发生网络错误: {e}"

    async def chat_loop(self):
        """Run an interactive chat loop"""
        while True:
            try:
                # 获取用户输入的查询
                query = input("\nQuery: ").strip()

                # 如果用户输入 'quit'，则退出循环
                if query.lower() == 'quit':
                    break

                # 处理用户查询
                response = await self.process_query(query)
                # 打印查询结果
                print("\n" + response)

            except Exception as e:
                # 记录错误信息
                logging.error(f"Error: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        # 关闭异步上下文栈，释放资源
        await self.exit_stack.aclose()


async def main():
    import sys
    # 如果命令行参数少于 2 个，提示用户输入服务器脚本路径并退出程序
    if len(sys.argv) < 2:
        logging.error("Usage: python mcp_client.py <path_to_server_script>")
        sys.exit(1)

    # 创建 MCPClient 对象
    client = MCPClient()
    try:
        # 连接到服务器
        await client.connect_to_server(sys.argv[1])
        # 启动聊天循环
        await client.chat_loop()
    finally:
        # 清理资源
        await client.cleanup()


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())