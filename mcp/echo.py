# echo.py

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Echo")

@mcp.tool()
def echo(text: str) -> str:
    """
    Echoes the input text back to the caller.
    """
    return f"You said: {text}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
