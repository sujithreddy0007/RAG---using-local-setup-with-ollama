from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    APP_NAME: str = "Session-Based Enterprise RAG"

    class Config:
        env_file = ".env"

settings = Settings()
