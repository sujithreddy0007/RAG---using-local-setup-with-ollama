from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db.session_store import session_exists
from app.rag.loader import load_text_from_file, chunk_text
from app.vectorstore.chroma import ChromaVectorStore

router = APIRouter()
vectorstore = ChromaVectorStore()

@router.post("/ingest")
async def ingest_document(session_id: str, file: UploadFile = File(...)):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Invalid session ID")

    file_bytes = await file.read()
    text = load_text_from_file(file_bytes, file.filename)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty document")

    chunks = chunk_text(text)

    vectorstore.add_texts(session_id, chunks)

    return {
        "status": "success",
        "chunks_added": len(chunks)
    }
