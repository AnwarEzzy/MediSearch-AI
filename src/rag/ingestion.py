import os
from pathlib import Path
from rich.console import Console
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter

console = Console()

def load_documents(data_dir: str) -> list[Document]:
    """
    Charge les documents (PDF, TXT, MD, etc.) depuis le dossier spécifié.
    
    Args:
        data_dir (str): Le chemin vers le dossier contenant les fichiers bruts.
        
    Returns:
        list[Document]: Une liste de documents LlamaIndex.
    """
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        console.print(f"[bold red]Erreur: Le dossier {data_dir} est vide ou n'existe pas.[/bold red]")
        return []
        
    console.print(f"Chargement des documents depuis [cyan]{data_dir}[/cyan]...")
    reader = SimpleDirectoryReader(input_dir=data_dir, required_exts=[".pdf", ".txt", ".md", ".json"])
    documents = reader.load_data()
    console.print(f"[green]✓ {len(documents)} documents chargés avec succès.[/green]")
    return documents

def chunk_documents(documents: list[Document], chunk_size: int = 512, overlap: int = 50) -> list[Document]:
    """
    Découpe les documents en morceaux (chunks) plus petits.
    
    Args:
        documents (list[Document]): Les documents à découper.
        chunk_size (int): Taille maximale d'un chunk.
        overlap (int): Nombre de tokens de chevauchement entre les chunks contigus.
        
    Returns:
        list[Document]: Les chunks sous forme de documents individuels (noeuds).
    """
    if not documents:
        return []
        
    console.print(f"Découpage des documents en chunks (size={chunk_size}, overlap={overlap})...")
    parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    
    # In LlamaIndex, parser.get_nodes_from_documents returns nodes. 
    nodes = parser.get_nodes_from_documents(documents)
    console.print(f"[green]✓ Documents découpés en {len(nodes)} chunks.[/green]")
    
    return nodes

