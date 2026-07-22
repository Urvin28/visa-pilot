from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.services.rag_services import RAGService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGService()


class Question(BaseModel):
    session_id: str
    question: str


@app.post("/chat")
def chat(request: Question):

    answer = rag.ask(
        session_id=request.session_id,
        question=request.question
    )

    return {
        "answer": answer
    }