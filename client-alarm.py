import asyncio
import requests
import logging
#typing模块的作用是支持类型提示，Optional[xx] 是指某个变量既可以是指定的类型xx，也可以是None
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

MODEL_SERVICE_URL = 'http://192.168.12.105:5670/api/v1/chat/completions'


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tool_descriptions = []
        self.tools_name = []

    def extract_tools(self, answer):
        try:
            # 如果 answer 是字符串，解析为 JSON
            if isinstance(answer, str):
                data = json.loads(answer)
            # 如果已经是字典，直接使用
            elif isinstance(answer, dict):
                data = answer
            else:
                return []  # 不是字典也不是字符串，返回空列表

            tool_list = []
            print(f"解析后的 data: {data}")  # 调试：打印解析后的数据

            # 情况1：平铺字典结构 {"tool1": {"dbid": 123}, "tool2": {"dbid": 456}}
            if isinstance(data, dict):
                for tool_name, tool_data in data.items():
                    if isinstance(tool_data, dict):  # 确保值是字典
                        dbid = tool_data.get("dbid")
                        if dbid is not None:
                            tool_list.append((tool_name, [dbid]))
                            print(f"已添加工具: {tool_name}, dbid: {dbid}")  # 调试日志

            return tool_list

        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")  # 调试日志
            return []

    async def call_mcp_tool(self, tool_name, tool_params):
        # 调用 MCP 会话中的工具
        if self.session:
            result = await self.session.call_tool(tool_name, *tool_params)
            return result
        return "未连接到服务器，无法调用工具"

    async def connect_to_server(self, server_script_path:str):
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
        
        command = "python" if is_python else "node"

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
        self.tools_name = [ tool.name for tool in tools]
        self.tool_descriptions = [ tool.description for tool in tools]
        # 记录日志，显示已连接到服务器以及可用的工具
        # logging.info(f"Connected to server with tools: {[tool.name for tool in tools]}")
        # print(f"tools:{tools}")
    async def process_query(self, query: str) -> str:
        """Process a query using the model service and available tools"""
        # 构建发送给模型的提示信息，包含用户问题和工具描述
        prompt = f"用户问题: {query}\n工具名字: {self.tools_name}工具描述: {self.tool_descriptions}\n请根据输入选择合适的工具及参数，并以json的格式返回,其中每个tool和对应的dbid放在一个键值对里"
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

        try:
            response = requests.post(MODEL_SERVICE_URL, json=request_data)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                try:
                    response = response.json()
                    answer = response.get('choices', [{}])[0].get('delta', {}).get('content', '')
                    print(f"answer:{answer}")
                    
                    tool_list = self.extract_tools(answer)
                    if tool_list:
                        print(f"从模型回答中提取的工具列表:{tool_list}")
                    else:
                        print("too_list为空")
                    # 调用 MCP 工具并获取结果
                    tool_results = []
                    for tool_name, tool_params in tool_list:
                        result = await self.call_mcp_tool(tool_name, tool_params)
                        tool_results.append(f"工具 {tool_name} 执行结果: {result}")

                    # 将工具执行结果反馈给大模型
                    new_prompt = f"用户问题: {query}\n工具执行结果: {tool_results}\n根据各个工具的执行结果以及工具描述，总结问题可能产生的原因"
                    new_request_data = request_data.copy()
                    new_request_data["user_input"] = new_prompt
                    new_response = requests.post(MODEL_SERVICE_URL, json=new_request_data)
                    new_response.encoding = 'utf-8'
                    if new_response.status_code == 200:
                        try:
                            new_response = new_response.json()
                            final_answer = new_response.get('choices', [{}])[0].get('delta', {}).get('content', '')
                            print(f"finallanswer:{final_answer}")
                            return final_answer
                        except ValueError as e:
                            return f"无法将新响应解析为 JSON 格式，详细错误信息: {e}"
                    else:
                        return f"请求模型失败，状态码为：{new_response.status_code}"

                except ValueError as e:
                    # 如果解析 JSON 失败，返回错误信息
                    return f"无法将响应解析为 JSON 格式，详细错误信息: {e}"
            else:
                return f"请求模型失败，状态码为：{response.status_code}"

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