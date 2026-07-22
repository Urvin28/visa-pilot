import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import VECTOR_STORE, EMBEDDING_MODEL


class Retriever:

    def __init__(self):

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.embeddings = np.load(VECTOR_STORE / "embeddings.npy")

        with open(VECTOR_STORE / "chunks.json", "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

    def search(self, query, top_k=3):

        query_embedding = self.model.encode([query])

        scores = cosine_similarity(query_embedding, self.embeddings)[0]

        top_indices = np.argsort(scores)[::-1][:top_k]

        return [self.chunks[i] for i in top_indices]
    


if __name__ == "__main__":

    retriever = Retriever()

    results = retriever.search(
        "When does H-1B registration start?"
    )

    for result in results:
        print(result)
        print("-" * 80)