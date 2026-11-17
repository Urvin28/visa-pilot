import json
import os

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from app.config import VECTOR_STORE

load_dotenv()


class Retriever:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for retrieval embeddings.")
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )

        try:
            with open(VECTOR_STORE / "chunks.json", "r", encoding="utf-8") as f:
                self.chunks = json.load(f)
            with open(VECTOR_STORE / "embeddings.json", "r", encoding="utf-8") as f:
                self.embeddings = np.asarray(json.load(f), dtype=np.float32)
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Vector store files are missing. Run `python -m app.ingestion.embedder`."
            ) from exc

        if not self.chunks or self.embeddings.ndim != 2:
            raise RuntimeError("Vector store is empty or malformed; rebuild it.")
        if len(self.chunks) != len(self.embeddings):
            raise RuntimeError(
                "Vector store chunk and embedding counts differ; rebuild it."
            )

    def search(self, query, top_k=3):

        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=query
        )

        query_embedding = np.array(response.data[0].embedding)

        denominator = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        scores = np.divide(
            self.embeddings @ query_embedding,
            denominator,
            out=np.zeros_like(denominator),
            where=denominator != 0,
        )

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [self.chunks[i] for i in top_indices]
