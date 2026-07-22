class PromptBuilder:

    @staticmethod
    def build(context, question, profile, history):

        return f"""
You are an expert U.S. immigration assistant.

Use the user's profile, conversation history and retrieved context.

If the answer is not in the context, say:
"I don't have enough information."

-------------------------
User Profile

{profile}

-------------------------
Conversation History

{history}

-------------------------
Context

{context}

-------------------------
Question

{question}

Answer:
"""
    
if __name__ == "__main__":

    prompt = PromptBuilder.build(
        context="Registration usually opens in March.",
        question="When does H-1B registration start?"
    )

    print(prompt)
    