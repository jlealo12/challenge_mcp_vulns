"""Versión protegida del agente de correos. Esta versión aplica los siguientes principios:
- Mínimo privilegio: se elimina el uso de la herramienta de shell, que está fuera del scope de la app
- Traceability: se habilitan logs de monitoreo del agente a un repositorio externo para validación y control
- Gating/HITL: se habilita vaidación humana antes de la ejecución de herramientas con acciones de modificación (C/UD)
"""

from strands import Agent
from strands.models.openai import OpenAIModel
import os

from dotenv import load_dotenv

from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from strands_tools import handoff_to_user

import logging
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_PATH = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "logs", "strands_agents_sdk.log")
)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_data)


# Create a file handler with JSON formatting
file_handler = logging.FileHandler(LOGS_PATH)
file_handler.setFormatter(JsonFormatter())

# Add the handler to the strands logger
logging.getLogger("strands").addHandler(file_handler)

streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client("http://localhost:8000/mcp")
)

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """Tu nombre es Melisa, eres una asistente virtual que ayuda a gestionar la bandeja de correo electrónico.
Debes ayudar al usuario a leer, priorizar y responder a sus correos electrónicos.
Antes de ejecutar las siguientes acciones, utiliza la herramienta 'handoff_to_user' para pedir autorización de ejecución al usuario:
- send_email"""

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
        system_prompt=SYSTEM_PROMPT,
        model=model,
        tools=tools + [handoff_to_user],
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
