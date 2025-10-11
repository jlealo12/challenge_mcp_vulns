from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import calculator
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

models = ["gpt-5-2025-08-07","gpt-5-mini-2025-08-07","gpt-4o","gpt-4.1-2025-04-14"]

model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    # **model_config
    model_id=models[2],
    params={
        "max_completion_tokens": 1000,
        # "temperature": 0.7,
    }
)

agent = Agent(model=model, tools=[calculator])
response = agent("What is 2+2")
print(response)
