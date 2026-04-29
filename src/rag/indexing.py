import os
import chromadb
from rich.console import Console
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings as LlamaIndexSettings
from src.config import get_settings

console = Console()
settings = get_settings()

def get_embed_model():
    """Initialise et retourne le modèle d'embeddings HuggingFace."""
    return HuggingFaceEmbedding(model_name=settings.embedding_model)

def init_chroma_client():
    """Initialise le client ChromaDB pointant vers le dossier permanent."""
    if not os.path.exists(settings.vectorstore_dir):
        os.makedirs(settings.vectorstore_dir)
    return chromadb.PersistentClient(path=settings.vectorstore_dir)

def build_index(nodes) -> VectorStoreIndex:
    """
    Construit l'index vectoriel à partir des chunks et le persiste dans ChromaDB.
    Si l'index existe déjà (collection non vide), on ne recrée pas tout.
    
    Args:
        nodes: La liste des nœuds (chunks) générés par le SentenceSplitter.
        
    Returns:
        VectorStoreIndex: L'index LlamaIndex.
    """
    # Configuration globale pour LlamaIndex
    LlamaIndexSettings.embed_model = get_embed_model()
    
    db = init_chroma_client()
    chroma_collection = db.get_or_create_collection(settings.chroma_collection_name)
    
    # On vérifie si y'a déjà des documents
    if chroma_collection.count() > 0:
        console.print("[yellow]Index existant détecté. Chargement de l'index sans re-traiter les chunks...[/yellow]")
        return load_index()
        
    console.print("Création et persistance du nouvel index vectoriel...")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context
    )
    console.print(f"[bold green]✓ Indexation terminée et persistante dans {settings.vectorstore_dir}.[/bold green]")
    return index

def load_index() -> VectorStoreIndex:
    """
    Charge l'index vectoriel existant depuis ChromaDB.
    
    Returns:
        VectorStoreIndex: L'index chargé.
    """
    LlamaIndexSettings.embed_model = get_embed_model()
    
    db = init_chroma_client()
    chroma_collection = db.get_or_create_collection(settings.chroma_collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )
    console.print(f"[green]✓ Index chargé avec succès avec {chroma_collection.count()} éléments.[/green]")
    return index

