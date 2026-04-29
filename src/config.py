import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM Settings
    groq_api_key: str | None = None
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:1b"
    
    # Embedding settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Storage settings
    data_dir: str = "./data/raw"
    vectorstore_dir: str = "./vectorstore"
    chroma_collection_name: str = "medisearch_docs"
    
    # RAG Settings
    chunk_size: int = 512
    chunk_overlap: int = 50
    similarity_top_k: int = 5

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

@lru_cache
def get_settings() -> Settings:
    """Returns a cached instance of the settings."""
    return Settings()

