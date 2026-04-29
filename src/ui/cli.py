import os
import sys
from pathlib import Path

# Fix for Windows console unicode errors (Banner issues)
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.orchestrator.orchestrator import MediSearchOrchestrator
from scripts.generate_sample_docs import main as generate_docs
from src.rag.ingestion import load_documents, chunk_documents
from src.rag.indexing import build_index
from src.config import get_settings

console = Console()
settings = get_settings()

def show_banner():
    banner = """
    [bold cyan]
    â–ˆâ–ˆâ–ˆâ•—   â–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•—  â–ˆâ–ˆâ•—
    â–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘
    â–ˆâ–ˆâ•”â–ˆâ–ˆâ–ˆâ–ˆâ•”â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—  â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘
    â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•  â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â•šâ•â•â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•  â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•‘
    â–ˆâ–ˆâ•‘ â•šâ•â• â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘
    â•šâ•â•     â•šâ•â•â•šâ•â•â•â•â•â•â•â•šâ•â•â•â•â•â• â•šâ•â•â•šâ•â•â•â•â•â•â•â•šâ•â•â•â•â•â•â•â•šâ•â•  â•šâ•â•â•šâ•â•  â•šâ•â• â•šâ•â•â•â•â•â•â•šâ•â•  â•šâ•â•
    [/bold cyan]
    [bold white]Assistant de Veille MÃ©dicale AutomatisÃ©e[/bold white]
    """
    console.print(banner)

def ingest_menu():
    console.print("\n[bold yellow]-- Ingestion des documents --[/bold yellow]")
    docs = load_documents(settings.data_dir)
    if not docs:
        console.print("[red]Aucun fichier brut trouvÃ©. Lancement de la gÃ©nÃ©ration...[/red]")
        generate_docs()
        docs = load_documents(settings.data_dir)
        
    nodes = chunk_documents(docs, settings.chunk_size, settings.chunk_overlap)
    build_index(nodes)

def search_menu():
    query = Prompt.ask("\n[bold green]Entrez votre question mÃ©dicale[/bold green]")
    if not query:
        return
        
    orchestrator = MediSearchOrchestrator()
    results = orchestrator.run(query)
    
    console.print("\n[bold success]=== RAPPORT FINAL ===[/bold success]")
    console.print(Panel(Markdown(results["final_report"]), title="Fiche de SynthÃ¨se", border_style="cyan"))
    
    score = results["validation_score"]
    color = "green" if score >= 70 else "red"
    console.print(f"\n[bold]Score de l'agent validateur:[/bold] [{color}]{score}/100[/{color}]")
    console.print(f"[bold]Validation Feedback:[/bold] {results['validation_feedback']}")
    
    save = Prompt.ask("\nSauvegarder ce rapport ? (o/n)", choices=["o", "n"], default="n")
    if save == "o":
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(exist_ok=True)
        # Format filename
        filename = query.replace(" ", "_").replace("?", "").replace("/", "_")[:30] + ".md"
        filepath = outputs_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(results["final_report"])
        console.print(f"[green]Rapport sauvegardÃ© sous {filepath}[/green]")

def main():
    while True:
        show_banner()
        console.print("\n[1] IngÃ©rer les documents")
        console.print("[2] Lancer une recherche (MediSearch)")
        console.print("[3] Quitter")
        
        choice = Prompt.ask("\nVotre choix", choices=["1", "2", "3"])
        
        if choice == "1":
            ingest_menu()
        elif choice == "2":
            search_menu()
        elif choice == "3":
            console.print("[dim]Au revoir.[/dim]")
            break

if __name__ == "__main__":
    main()

