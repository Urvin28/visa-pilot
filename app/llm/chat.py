from ollama import chat

response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "What is H-1B?"
        }
    ]
)

print(response["message"]["content"])