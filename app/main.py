from fastapi import FastAPI
from app.api import session, ingest, chat   # ✅ add chat
from app.db.session_store import init_db

app = FastAPI(title="Enterprise Session-Based RAG")

init_db()

app.include_router(session.router)
app.include_router(ingest.router)
app.include_router(chat.router)             # ✅ add this
