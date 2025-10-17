import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mail_client import _get_emails, _search_email, _send_email

from fastmcp import FastMCP

mcp = FastMCP("Meli MCP")


@mcp.tool
def list_emails() -> list[dict]:
    """Returns the list of all available emails"""
    return _get_emails()


@mcp.tool
def get_email(id: str) -> dict:
    """Search and return an email in the database by using the id"""
    return _search_email(id)


@mcp.tool
def send_email(to: str, subject: str, body: str) -> dict:
    """Sends an email to a user."""
    return _send_email(to, subject, body)


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
