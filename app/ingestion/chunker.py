from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load one document
project_folder = Path(__file__).parent.parent

file_path = project_folder / "knowledge_base" / "uscis" / "h1b.md"

text = file_path.read_text(encoding="utf-8")

# Create splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Split document
chunks = splitter.split_text(text)

print(f"Total chunks: {len(chunks)}")
print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n------ Chunk {i+1} ------\n")
    print(chunk[:300])