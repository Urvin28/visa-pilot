from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"

VECTOR_STORE = PROJECT_ROOT / "vector_store"

MODEL_NAME = "llama3.2:3b"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"