import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.logging import logger

class ChromaVectorStore:
    def __init__(self):
        logger.info("Initializing ChromaDB")
        self.client = chromadb.Client(
            Settings(
                persist_directory=settings.CHROMA_PERSIST_DIR,
                anonymized_telemetry=False
            )
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def _get_collection(self, session_id: str):
        return self.client.get_or_create_collection(
            name=f"session_{session_id}"
        )

    def add_texts(self, session_id: str, texts: list[str]):
        collection = self._get_collection(session_id)
        embeddings = self.embedding_model.encode(texts).tolist()

    # IMPORTANT: IDs must be unique across ingests
        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]

        collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids
        )

        logger.info(f"Stored {len(texts)} chunks for session {session_id}")

    def query(self, session_id: str, query: str, top_k: int = 4) -> list[str]:
        collection = self._get_collection(session_id)
        query_embedding = self.embedding_model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"][0] if results["documents"] else []
