import sys
from pathlib import Path
from rich.console import Console

# On s'assure que 'src' est dans le python path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import get_settings
from src.rag.ingestion import load_documents, chunk_documents
from src.rag.indexing import build_index
from src.rag.retrieval import create_query_engine, retrieve_context

console = Console()
settings = get_settings()

def main():
    console.print("\n[bold magenta]--- TEST DU PIPELINE RAG MEDISEARCH ---[/bold magenta]\n")
    
    # 1. Chargement et chunking
    docs = load_documents(settings.data_dir)
    if not docs:
        console.print("[red]Veuillez générer les documents de test d'abord avec `python scripts/generate_sample_docs.py`[/red]")
        return
        
    nodes = chunk_documents(docs, settings.chunk_size, settings.chunk_overlap)
    
    # 2. Indexation
    index = build_index(nodes)
    
    # 3. Création Query Engine
    query_engine = create_query_engine(index)
    
    # 4. Tests
    test_queries = [
        "Quels sont les effets des probiotiques sur l'immunité ?",
        "Comment le manque de sommeil influence-t-il l'efficacité des vaccins ?",
        "Quels sont les risques des thérapies CAR-T et pour quels cancers sont-elles utilisées ?"
    ]
    
    console.print("\n[bold blue]=== TEST DES REQUÊTES ===[/bold blue]")
    for query in test_queries:
        console.print(f"\n[bold yellow]Recherche:[/bold yellow] {query}")
        result = retrieve_context(query, query_engine)
        
        # Affichage d'un aperçu
        if result and "Aucun contexte" not in result:
            console.print("[green]Résultats trouvés ![/green]")
            # Affiche les 300 premiers caractères pour voir
            console.print(f"[dim]{result[:300]}...[/dim]")
        else:
            console.print("[red]Aucun résultat.[/red]")

if __name__ == "__main__":
    main()

