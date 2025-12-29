from fastapi import APIRouter
import uuid
from app.db.session_store import create_session

router = APIRouter()

@router.post("/session/create")
def create_new_session():
    session_id = str(uuid.uuid4())
    create_session(session_id)
    return {"session_id": session_id}
