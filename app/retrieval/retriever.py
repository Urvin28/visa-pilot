import json

from openai import OpenAI

from app.config import VECTOR_STORE

import os
from dotenv import load_dotenv

load_dotenv()


class Retriever:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        with open(VECTOR_STORE / "chunks.json", "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        with open(VECTOR_STORE / "embeddings.json", "r") as f:
            self.embeddings = json.load(f)

    def search(self, query, top_k=3):

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )

        query_embedding = response.data[0].embedding

        scores = []

        for embedding in self.embeddings:
            score = sum(a * b for a, b in zip(query_embedding, embedding))
            scores.append(score)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        return [self.chunks[i] for i in top_indices]