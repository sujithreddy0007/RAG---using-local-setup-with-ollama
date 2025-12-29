import requests
from app.core.logging import logger

class OllamaLLM:
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            return response.json()["response"].strip()
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "LLM is currently unavailable."
