"""Simple guardrails implementation"""

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI()


def apply_guardrails(input_: str) -> dict:
    """Applies moderation endpoint to a text input"""
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=input_,
    )
    return response
