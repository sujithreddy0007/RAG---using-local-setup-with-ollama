from app.rag.retriever import Retriever
from app.rag.prompt import build_prompt
from app.rag.llm import OllamaLLM
from app.core.logging import logger

class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = OllamaLLM()

    def run(self, session_id: str, question: str) -> str:
        context = self.retriever.retrieve(session_id, question)
        prompt = build_prompt(context, question)

        logger.info(
            "Using document context" if context else "Using general LLM knowledge"
        )

        return self.llm.generate(prompt)
