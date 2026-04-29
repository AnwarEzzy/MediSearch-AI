import os
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from src.config import get_settings

settings = get_settings()

def get_llm():
    """
    Retourne le LLM configuré.
    Fallback: Si GROQ_API_KEY est défini, utilise Groq (rapide et gratuit),
    sinon utilise Ollama en local (llama3.2:1b).
    """
    groq_api_key = settings.groq_api_key or os.getenv("GROQ_API_KEY")
    
    if groq_api_key and groq_api_key.strip():
        # Utilisation de Groq
        return ChatGroq(
            api_key=groq_api_key,
            model_name="llama-3.1-8b-instant", # modèle par défaut pour Groq
            temperature=0
        )
    else:
        # Utilisation de Ollama en local
        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0
        )

