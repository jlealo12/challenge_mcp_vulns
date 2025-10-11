import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mail_client import get_emails, search_email

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


@mcp.tool
def list_emails() -> list[dict]:
    """Returns the list of all available emails"""
    return get_emails()


@mcp.tool
def get_email(id: str) -> list[dict]:
    """Search and return an email in the database by using the id"""
    return search_email(id)


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
