import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(fn_name: str, fn_input: dict = None):
    async with client:
        result = await client.call_tool(fn_name, fn_input)
        print(result)


asyncio.run(call_tool("list_emails"))
asyncio.run(call_tool("get_email", {"id": "email001"}))
asyncio.run(call_tool("get_email", {"id": "email005"}))
asyncio.run(
    call_tool(
        "send_email",
        {"to": "ejemplo@ejemplo.com", "subject": "Ejemplo", "body": "Body ejemplo"},
    )
)
