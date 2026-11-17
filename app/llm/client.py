import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
    """Text generation client using the OpenAI Responses API."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Add it to .env locally or to the "
                "visa-pilot-api service environment in Render."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_CHAT_MODEL", "gpt-5.4-mini")

    def generate(self, system_prompt, user_prompt):
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_prompt,
        )
        return response.output_text
