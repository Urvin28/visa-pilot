from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

project_folder = Path(__file__).parent.parent

# Load embeddings
embeddings = np.load(project_folder / "vector_store" / "embeddings.npy")

# Load chunks
with open(project_folder / "vector_store" / "chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# User question
query = "When does H-1B registration start?"

# Embed question
query_embedding = model.encode([query])

# Compute similarity
scores = cosine_similarity(query_embedding, embeddings)[0]

# Top 3 matches
top_indices = np.argsort(scores)[::-1][:3]

print("\nTop Results:\n")

for i in top_indices:
    print(f"Score: {scores[i]:.4f}")
    print(chunks[i][:500])
    print("-" * 80)