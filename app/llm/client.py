from ollama import chat
from app.config import MODEL_NAME


class LLMClient:

    def __init__(self):
        self.model = MODEL_NAME

    def generate(self, system_prompt, user_prompt):

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response["message"]["content"]
    

if __name__ == "__main__":

    llm = LLMClient()

    answer = llm.generate(
        "You are a helpful assistant.",
        "Say hello in one sentence."
    )

    print(answer)
    