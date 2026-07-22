import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, system_prompt, user_prompt):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.2,
        )

        return response.choices[0].message.content