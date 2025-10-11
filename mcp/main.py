from fastmcp import FastMCP

mcp = FastMCP("Meli MCP")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("Executing call to add tool from MCP")
    return a + b

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
