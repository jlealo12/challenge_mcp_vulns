from strands import Agent
from strands.models.openai import OpenAIModel
import os

from dotenv import load_dotenv

from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from strands_tools import shell

streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client("http://localhost:8000/mcp")
)

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """Tu nombre es Melisa, eres una asistente virtual que ayuda a gestionar la bandeja de correo electrónico.
Debes ayudar al usuario a leer, priorizar y responder a sus correos electrónicos."""

model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_completion_tokens": 1000,
        "temperature": 0.7,
    },
)

with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()

    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        model=model,
        tools=tools + [shell],
        callback_handler=None,
    )

    try:
        # Run the conversarion loop
        while True:
            print("=" * 30)
            query_ = input("Enter your message here: ")
            print("=" * 30)
            print(f"Query: {query_}")
            response = agent(query_)
            print(f"Response: {response}")
    except KeyboardInterrupt:
        print("\n\nGracias por conversar. ¡Hasta pronto! 👋")
