import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        # result = await client.call_tool("greet", {"name": name})
        # result = await client.call_tool("list_emails")
        # result = await client.call_tool("get_email", {"id": "email001"})
        result = await client.call_tool("get_email", {"id": "email005"})
        print(result)

asyncio.run(call_tool("Ford"))
