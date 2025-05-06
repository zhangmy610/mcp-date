from mcp.server import FastMCP
from base import DbTypeAgentUrlMode
from config import Config
import requests
import logging
from datetime import datetime,timedelta

CFG = Config()

mcp = FastMCP("Alarm",port=9008)

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
        logging.info("登录成功")
        return res.json().get("data").get("token"), res.cookies.get("SESSION")
    return None, None

  

# @mcp.tool(description="检查主机资源的使用情况")
# def check_zhuji_resource(dbid,startTime,endTime):
    # try:
    #     if dbid == "请输入dbid":
    #         return "请输入dbid"
    #     if dbid is None:
    #         return f"dbid为 {dbid}的数据库不存在"
    #     if startTime == "请输入开始时间，例如：2025-04-30 07:56:17":
    #         return "请输入开始时间，例如：2025-04-30 07:56:17"
    #     if endTime == "请输入开始时间，例如：2025-04-30 07:56:17":
    #         return "请输入开始时间，例如：2025-04-30 07:56:17"
        
    #     hostId = 
    #     token, session = get_token()
    #     if token is None:
    #         return "获取调用接口的token失败"
        
    #     headers = {
    #         "access_token": token,
    #         "cookie": f"SESSION={session}"
    #     }
    #     url = f"http://192.168.12.84:8520/gateway/monitor-interactive-service/host/memory/" \
    #           f"?startTime={startTime}&endTime={endTime}&hostId={hostId}"
    #     logging.info(f'调用dmp接口获取参数的url为：{url}')
    #     response = requests.get(url, headers=headers)
    #     if response.status_code != 200:
    #         return "执行获取数据库信息失败"

    # except Exception as e:
    #     logging.exception(f"根据数据库别名和参数类型获取数据库的所有参数信息 的工具执行失败，错误信息为：{str(e)}")
    #     return f"agent工具执行失败"

@mcp.tool(description="检查数据库资源容量的使用情况")
def check_database_resource(dbid):
    try:
        if dbid == "请输入dbid":
            return "请输入dbid"
        if dbid is None:
            return f"dbid为 {dbid}的数据库不存在"
        
        token, session = get_token()
        if token is None:
            return "获取调用接口的token失败"
        
        headers = {
            "access_token": token,
            "cookie": f"SESSION={session}"
        }
        logging.info(f"access_token: {token}")
        logging.info(f"cookie: {session}")
        url = f"http://192.168.1.43:8960/gateway/monitor-interactive-service/database/db2/capacity/capacity-info?dbid={dbid}"
        logging.info(f'调用dmp接口获取参数的url为：{url}')
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "执行获取数据库信息失败"
        response_json = response.json()
        logging.info(f'调用dmp 接口返回结果为：{response_json}')
        data = response_json.get("data")
        logging.info(f"data: {data}")
        return data

    except Exception as e:
        logging.exception(f"根据数据库别名和参数类型获取数据库的所有参数信息 的工具执行失败，错误信息为：{str(e)}")
        return f"agent工具执行失败"

@mcp.tool(description="检查QPS负载")
def check_qps(dbid):
    try:
        if dbid == "请输入dbid":
            return "请输入dbid"
        if dbid is None:
            return f"dbid为 {dbid}的数据库不存在"
        startTime=(datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        endTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        token, session = get_token()
        if token is None:
            return "获取调用接口的token失败"
        
        headers = {
            "access_token": token,
            "cookie": f"SESSION={session}"
        }
        url = f"http://192.168.1.43:8960/gateway/monitor-interactive-service/database/db2/perf-analysis/workload-qps-chart"\
              f"?dbid={dbid}&startTime={startTime}&endTime={endTime}&member=0"
        logging.info(f'调用dmp接口获取参数的url为：{url}')
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "执行获取数据库信息失败"
        response_json = response.json()
        logging.info(f'调用dmp 接口返回结果为：{response_json}')
        data = response_json.get("data")
        logging.info(f"data: {data}")
        return data
    except Exception as e:
        logging.exception(f"根据数据库别名和参数类型获取数据库的所有参数信息 的工具执行失败，错误信息为：{str(e)}")
        return f"agent工具执行失败"

if __name__ == "__main__":
    mcp.run(transport='sse')