"""Build the JSON vector store from every Markdown file in knowledge_base.

Run from the project root with: python -m app.ingestion.embedder
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"
VECTOR_STORE = PROJECT_ROOT / "vector_store"
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def build_vector_store():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to build the vector store.")

    files = sorted(KNOWLEDGE_BASE.rglob("*.md"))
    if not files:
        raise RuntimeError(f"No Markdown source documents found under {KNOWLEDGE_BASE}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8").strip()
        if text:
            chunks.extend(splitter.split_text(text))

    if not chunks:
        raise RuntimeError("The Markdown files contained no text to index.")

    client = OpenAI(api_key=api_key)
    embeddings = []
    # Batch requests reduce latency and avoid one API call per chunk.
    for start in range(0, len(chunks), 100):
        batch = chunks[start : start + 100]
        result = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        embeddings.extend(item.embedding for item in result.data)

    if len(chunks) != len(embeddings):
        raise RuntimeError("Embedding count did not match the chunk count.")

    VECTOR_STORE.mkdir(parents=True, exist_ok=True)
    (VECTOR_STORE / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (VECTOR_STORE / "embeddings.json").write_text(
        json.dumps(embeddings), encoding="utf-8"
    )
    print(f"Indexed {len(chunks)} chunks from {len(files)} Markdown documents.")


if __name__ == "__main__":
    build_vector_store()
