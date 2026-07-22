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


from fastapi import HTTPException
import traceback


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        answer = rag.ask(
            request.session_id,
            request.question
        )

        return {"answer": answer}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))