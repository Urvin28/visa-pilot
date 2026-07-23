import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

project_folder = Path(__file__).parent.parent.parent
file_path = project_folder / "knowledge_base" / "uscis" / "h1b.md"

text = file_path.read_text(encoding="utf-8")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = splitter.split_text(text)

embeddings = []

for chunk in chunks:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    embeddings.append(response.data[0].embedding)

with open(project_folder / "vector_store" / "chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

with open(project_folder / "vector_store" / "embeddings.json", "w") as f:
    json.dump(embeddings, f)

print("Vector store created.")