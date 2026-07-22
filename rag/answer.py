from pathlib import Path
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from ollama import chat
from app.memory.conversation import ConversationMemory
# -------------------------
# Load embedding model
# -------------------------
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

project_folder = Path(__file__).parent.parent
memory = ConversationMemory()

# -------------------------
# Load vector store
# -------------------------
embeddings = np.load(project_folder / "vector_store" / "embeddings.npy")

with open(project_folder / "vector_store" / "chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# -------------------------
# Ask question
# -------------------------
query = input("Ask a question: ")

# -------------------------
# Embed question
# -------------------------
query_embedding = embedding_model.encode([query])

scores = cosine_similarity(query_embedding, embeddings)[0]

# Top 1 chunk
top_indices = np.argsort(scores)[::-1][:1]

context = "\n\n".join(chunks[i] for i in top_indices)

print("\n================ CONTEXT ================\n")
print(context)
print("\n=========================================\n")

# -------------------------
# LLM
# -------------------------
response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": """You are an expert U.S. immigration assistant.

You MUST answer ONLY from the provided context.

Rules:
- If the answer is in the context, answer directly.
- Do not say "I don't have enough information" if the answer is clearly present.
- Do not use outside knowledge.
- Keep answers concise.
"""
        },
        {
            "role": "user",
            "content": f"""
Context:
{context}

Question:
{query}

Answer:
"""
        }
    ]
)

print("\n================ ANSWER ================\n")
print(response["message"]["content"])