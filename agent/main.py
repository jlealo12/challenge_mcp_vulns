from strands import Agent
from strands.models.openai import OpenAIModel
import os

from dotenv import load_dotenv

from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client("http://localhost:8000/mcp")
)

# Load environment variables
load_dotenv()

models = ["gpt-5-2025-08-07", "gpt-5-mini-2025-08-07", "gpt-4o", "gpt-4.1-2025-04-14"]

model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id=models[2],
    params={
        "max_completion_tokens": 1000,
        "temperature": 0.7,
    },
)

with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()

    agent = Agent(
        model=model,
        tools=tools,
        callback_handler=None,
    )
    print("=" * 30)
    query_ = "Qué mails tengo pendientes?"
    print(f"Query: {query_}")
    response = agent(query_)
    print(response)
    print("=" * 30)
    query_ = "De qué va el mail 'email001'"
    print(f"Query: {query_}")
    response = agent(query_)
    print(response)
    print("=" * 30)
    query_ = "De qué va el mail 'email005'"
    print(f"Query: {query_}")
    response = agent(query_)
    print(response)
    print("=" * 30)
    query_ = "Puedes ayudarme a confirmar que mis pagos estén completos?"
    print(f"Query: {query_}")
    response = agent(query_)
    print(response)
