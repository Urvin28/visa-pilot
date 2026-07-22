from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Load document
project_folder = Path(__file__).parent.parent
file_path = project_folder / "knowledge_base" / "uscis" / "h1b.md"

text = file_path.read_text(encoding="utf-8")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(text)

# Generate embeddings
embeddings = model.encode(chunks)

print(f"Chunks: {len(chunks)}")
print(f"Embedding shape: {embeddings.shape}")

import json
import numpy as np

# Save embeddings
np.save(project_folder / "vector_store" / "embeddings.npy", embeddings)

# Save chunks
with open(project_folder / "vector_store" / "chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("Saved vector store!")