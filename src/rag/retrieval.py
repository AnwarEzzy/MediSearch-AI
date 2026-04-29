from llama_index.core import VectorStoreIndex
from src.config import get_settings

settings = get_settings()

def create_query_engine(index: VectorStoreIndex):
    """
    Retourne un retriever simple sans LLM (LangChain gère les LLMs).
    """
    return index.as_retriever(
        similarity_top_k=settings.similarity_top_k,
    )

def retrieve_context(query: str, query_engine) -> str:
    """
    Exécute une recherche sémantique et retourne les passages avec leurs sources.
    """
    # query_engine est en réalité un retriever ici
    nodes = query_engine.retrieve(query)

    if not nodes:
        return "Aucun contexte pertinent trouvé dans la base de connaissances médicale locale."

    formatted_context = "Voici les extraits pertinents trouvés dans le corpus médical:\n\n"
    for i, node in enumerate(nodes):
        source = node.metadata.get('file_name', 'Source inconnue')
        score = node.score if node.score else 0.0
        formatted_context += f"--- Extrait {i+1} (Source: {source}, Pertinence: {score:.2f}) ---\n"
        formatted_context += f"{node.text}\n\n"

    return formatted_context
