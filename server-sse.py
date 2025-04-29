# 从 typing 模块导入 Any 类型，表示任意类型
from typing import Any
from mcp.server.fastmcp import FastMCP
import pymysql
import logging
import requests
from typing_extensions import Annotated, Doc

from base import DbTypeAgentUrlMode
from config import Config

CFG = Config()
logger = logging.getLogger(__name__)
# 配置日志记录，设置日志级别为 INFO，即记录信息性消息
logging.basicConfig(level=logging.INFO)

# 创建 FastMCP 服务器实例，命名为 "MySQL_API"
mcp = FastMCP("MySQL_API")
#mcp = FastMCP("MySQL_API",port=9008)

mydb = pymysql.connect(
    host="192.168.1.222",
    user="testdbmon",
    password="testdbmon",
    database="test"
)
# 创建游标对象，用于执行 SQL 语句
mycursor = mydb.cursor()

def execute_query(query):
    try:
        # 执行 SQL 查询
        mycursor.execute(query)
        # 获取查询结果
        results = mycursor.fetchall()
        return results
    except pymysql.err.ProgrammingError as e:
        # 判断是否是表不存在的错误
        if e.args[0] == 1146:
            # 记录错误信息
            logging.error("错误：表不存在。")
            return "错误：表不存在。"
        else:
            # 记录查询出错信息
            logging.error(f"查询出错: {e}")
            return f"查询出错: {e}"
    except Exception as e:
        # 记录其他异常信息
        logging.error(f"查询出错: {e}")
        return f"查询出错: {e}"

@mcp.tool()
async def query_table(query: str) -> str:
    """用于执行 SQL 查询语句，返回查询结果
    Args:
        query: SQL 查询语句
    """
    # 调用 execute_query 函数执行查询
    results = execute_query(query)
    # 如果结果是字符串类型，直接返回
    if isinstance(results, str):
        return results
    # 将查询结果转换为字符串并按行拼接
    return '\n'.join(str(row) for row in results)

@mcp.tool()
async def query_explain(query: str) -> str:
    """用于查询 SQL 语句的执行计划
    Args:
        query: SQL 查询语句
    """
    # 构建 EXPLAIN 查询语句
    explain_query = f"EXPLAIN {query}"
    # 调用 execute_query 函数执行查询
    results = execute_query(explain_query)
    # 如果结果是字符串类型，直接返回
    if isinstance(results, str):
        return results
    # 将查询结果转换为字符串并按行拼接
    return '\n'.join(str(row) for row in results)

@mcp.tool()
async def get_table_creation_statement(table_name: str) -> str:
    """用于返回指定表的创建语句
    Args:
        table_name: 表名
    """
    # 构建 SHOW CREATE TABLE 查询语句
    query = f"SHOW CREATE TABLE {table_name}"
    # 调用 execute_query 函数执行查询
    results = execute_query(query)
    # 如果结果是字符串类型，直接返回
    if isinstance(results, str):
        return results
    # 如果查询结果不为空，返回表的创建语句
    if results:
        return results[0][1]
    # 如果未找到表的创建语句，返回提示信息
    return "未找到表的创建语句。"

@mcp.tool(description="根据数据库别名和参数类型获取数据库的所有参数信息.")
def get_database_variable_info(
        db_alias: Annotated[str, Doc("数据库别名")],
        parameter_type: Annotated[str, Doc("数据库参数类型.")] = "",
) -> str:
    """根据数据库ID和参数类型获取数据库的所有参数信息"""
    try:
        if db_alias == "请输入数据库别名":
            return "请输入数据库别名 "
        token, session = get_token()
        if token is None:
            return "获取调用接口的token失败"
        db_id, db_type  = get_dbid_by_db_alias(token, session, db_alias)
        if db_id is None:
            return f"数据库别名为**{db_alias}**的数据库不存在"
        headers = {
            "access_token": token,
            "cookie": f"SESSION={session}"
        }
        url = f"http://192.168.12.84:8520/gateway/monitor-interactive-service/database/mysql/" \
              f"parameter-manage/global-variables?dbid={db_id}&parameterType={parameter_type}"
        logger.info(f'调用dmp接口获取参数的url为：{url}')
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "执行获取数据库所有参数信息失败"
        response_json = response.json()
        logger.info(f'调用dmp 接口返回结果为：{response_json}')
        data = response_json.get("data")
        logger.info(f"data: {data}")
        result = ""
        for item in data:
            result = result + f"**参数名称**：{item.get('Variable_name')}，**当前参数值**：{item.get('Value')} <br>"
        return result
    except Exception as e:
        logger.exception(f"根据数据库别名和参数类型获取数据库的所有参数信息 的工具执行失败，错误信息为：{str(e)}")
        return f"agent工具执行失败"

@mcp.tool(description="获取MySQL容量信息")
def get_database_info(db_alias: str) -> str:
    try:
        if db_alias == "请输入数据库别名":
            return "请输入数据库别名"
        token, session = get_token()
        if token is None:
            return "获取调用接口的token失败"
        db_id, db_type  = get_dbid_by_db_alias(token, session, db_alias)
        if db_id is None:
            return f"数据库别名为**{db_alias}**的数据库不存在"
        headers = {
            "access_token": token,
            "cookie": f"SESSION={session}"
        }
        url = f"http://192.168.12.84:8520/gateway/monitor-interactive-service/database/mysql/" \
              f"capacity/capacity-info?dbid={db_id}"
        logger.info(f'调用dmp接口获取参数的url为：{url}')
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "执行获取数据库所有参数信息失败"
        response_json = response.json()
        logger.info(f'调用dmp 接口返回结果为：{response_json}')
        data = response_json.get("data")
        logger.info(f"data: {data}")
        result = ""
        for item in data:
            result = result + f"**数据库名**：{item.get('name')}，**容量大小**：{item.get('usedSize')} <br>"
        return result
    except Exception as e:
        logger.exception(f"根据数据库别名和参数类型获取数据库的所有参数信息 的工具执行失败，错误信息为：{str(e)}")
        return f"agent工具执行失败"   

def get_dbid_by_db_alias(token, session, db_alias):
    url = DbTypeAgentUrlMode.GET_DBID_BY_ALIAS_URL.format(CFG.DMP_AGENT_URL)
    headers = {
        "access_token": token,
        "cookie": f"SESSION={session}"
    }
    data = {
        "pageNum": 1,
        "pageSize": 15,
        "isAsc": True,
        "sort": "",
        "dbAlias": db_alias,
    }
    res = requests.post(url=url, json=data, headers=headers)
    if res.status_code == 200:
        logger.info("获取数据库ID成功}")
        logger.info(f'调用dmp 获取数据库ID的接口返回结果为：{res.json()}')
        db_info_list = res.json().get("data").get("list")
        if db_info_list is None or len(db_info_list) == 0:
            return None, None
        for db_info in db_info_list:
            alias = db_info.get("dbAlias")
            if alias == db_alias:
                dbid = db_info.get("dbid")
                db_type = db_info.get("dbType")
                logger.info(f"数据库ID为：{dbid}, 数据库别名为：{alias}")
                return dbid, db_type
        return None, None
    else:
        return None, None

def get_token():
    url = DbTypeAgentUrlMode.LOGIN_IN_URL.format(CFG.DMP_AGENT_URL)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    params = {
        "username": CFG.DMP_AGENT_USER_NAME,
        "password": CFG.DMP_AGENT_PASSWORD,
        "verify": ""
    }
    res = requests.post(url=url, json=params, headers=headers)
    if res.status_code == 200:
        logger.info("登录成功,")
        return res.json().get("data").get("token"), res.cookies.get("SESSION")
    return None, None

if __name__ == "__main__":
    # Initialize and run the server
    # 启动 FastMCP 服务器，使用 stdio 传输方式
    mcp.run(transport='stdio')
#	mcp.run(transport='sse')
