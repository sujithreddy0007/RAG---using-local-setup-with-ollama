from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.session_store import session_exists
from app.rag.pipeline import RAGPipeline

router = APIRouter()
rag = RAGPipeline()

class ChatRequest(BaseModel):
    session_id: str
    question: str

@router.post("/chat")
def chat(req: ChatRequest):
    if not session_exists(req.session_id):
        raise HTTPException(status_code=404, detail="Invalid session ID")

    answer = rag.run(req.session_id, req.question)
    return {"answer": answer}
