# VisaPilot

VisaPilot is a small FastAPI and React chat app for answering U.S. immigration questions from a locally stored knowledge base. It retrieves relevant chunks using OpenAI embeddings and drafts the response with an OpenAI chat model.

## Configure the API

Copy `.env.example` to `.env` and set `OPENAI_API_KEY` to an API key from the OpenAI API platform. The API key used by this app must have API access and billing enabled; a ChatGPT subscription does not provide API credits. `OPENAI_CHAT_MODEL` and `OPENAI_EMBEDDING_MODEL` can be changed in `.env` if needed.

For Render, open the `visa-pilot-api` web service, go to **Environment**, add `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL` (`gpt-5.4-mini`), and `OPENAI_EMBEDDING_MODEL` (`text-embedding-3-small`), then save and redeploy. Do not put API keys in frontend code or commit `.env`.

## Rebuild retrieval data

After changing or refreshing source documents, run this from the project root:

```powershell
python -m app.ingestion.embedder
```

The command reads every `*.md` file under `knowledge_base/`, creates chunks, requests embeddings in batches, and replaces `vector_store/chunks.json` and `vector_store/embeddings.json`. It needs `OPENAI_API_KEY` and incurs embedding API usage. Commit the regenerated vector-store files so Render receives the updated index on deploy.

The app validates that chunk and embedding counts match when it starts. The embedder and runtime retriever use the same `OPENAI_EMBEDDING_MODEL` setting; if changing that model, rebuild the vector store before deploying.

## Run locally

```powershell
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```

Run the frontend separately from `frontend/` with `npm install` and `npm run dev`.
