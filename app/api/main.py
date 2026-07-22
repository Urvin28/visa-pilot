from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import traceback

from app.services.rag_services import RAGService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGService()


class ChatRequest(BaseModel):
    session_id: str
    question: str


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        answer = rag.ask(
            request.session_id,
            request.question
        )

        return {
            "answer": answer
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )