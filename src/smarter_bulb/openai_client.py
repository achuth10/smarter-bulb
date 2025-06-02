"""
OpenAI API client
"""

from openai import OpenAI

from config import OPENAI_CONFIG


openai_client = OpenAI(
    api_key=OPENAI_CONFIG["API_KEY"],
)
