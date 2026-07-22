import json

from app.llm.client import LLMClient


class UserInfoExtractor:

    def __init__(self):
        self.llm = LLMClient()

    def extract(self, message):

        system_prompt = """
You extract user information.

Return ONLY valid JSON.

If nothing is found return:

{}
"""

        user_prompt = f"""
Extract the following if present:

- visa
- university
- graduation_date
- stem
- major

Message:

{message}
"""

        response = self.llm.generate(
            system_prompt,
            user_prompt
        )

        try:
            return json.loads(response)
        except:
            return {}