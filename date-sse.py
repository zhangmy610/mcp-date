# from mcp.server.fastmcp import FastMCP
from mcp.server import FastMCP
from datetime import datetime

# mcp = FastMCP("GetCurrentTime")
mcp = FastMCP("GetCurrentTime", port=9009)

@mcp.tool(description="当前时间")
def get_current_time():
    now = datetime.now()

    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    current_time = {"time": formatted_time}
    return current_time

if __name__ =="__main__":
    print("Starting MCP Server...")
    # mcp.run(transport='stdio')
    mcp.run(transport='sse')
