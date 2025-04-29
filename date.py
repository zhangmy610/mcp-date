from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("GetCurrentTime")

@mcp.tool()
def get_current_time():
    now = datetime.now()

    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    current_time = {"time": formatted_time}
    return current_time

if __name__ =="__main__":
    print("Starting MCP Server...")
    mcp.run(transport='stdio')
