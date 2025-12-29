from app.vectorstore.chroma import ChromaVectorStore
from app.core.logging import logger

class Retriever:
    def __init__(self):
        self.vectorstore = ChromaVectorStore()

    def retrieve(self, session_id: str, question: str, top_k: int = 4) -> list[str]:
        logger.info(f"Retrieving context for session {session_id}")
        return self.vectorstore.query(session_id, question, top_k)
