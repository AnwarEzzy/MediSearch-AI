"""
MediSearch — Point d'entrée principal du projet.

Usage:
    python main.py           # menu interactif
    python main.py --cli     # directement l'analyse patients (terminal)
    python main.py --gradio  # directement l'interface Gradio (web)
"""
import sys
import os
from pathlib import Path

# Force UTF-8 console on Windows (sans remplacer sys.stdout)
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Ajouter la racine au path
sys.path.append(str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from rich.table import Table

console = Console(highlight=False)


def display_banner():
    console.print()
    console.print(Panel(
        "[bold cyan]MediSearch — Assistant de Veille Medicale[/bold cyan]\n"
        "[dim]Systeme Multi-Agents | Groq Llama 3.1 | RAG Medical[/dim]\n\n"
        "[white]Choisissez le mode de lancement :[/white]",
        border_style="cyan",
        padding=(1, 6)
    ))
    console.print()


def display_mode_menu():
    table = Table(box=box.ROUNDED, border_style="blue", header_style="bold blue", show_header=False, padding=(0, 2))
    table.add_column("Option", style="bold yellow", width=6, justify="center")
    table.add_column("Mode",   style="bold white",  width=28)
    table.add_column("Description", style="dim",    width=50)

    table.add_row("[1]", "Analyse Patients (CLI)",
                  "Interface terminal : selectionner 1 ou N patients et generer des fiches medicales.")
    table.add_row("[2]", "Veille Medicale (Gradio)",
                  "Interface web : poser une question medicale et obtenir une synthese multi-agents.")
    table.add_row("[3]", "Quitter", "")

    console.print(table)
    console.print()


def run_cli():
    """Lance l'interface CLI d'analyse des patients."""
    console.print("[dim]Lancement de l'analyse patients en mode terminal...[/dim]\n")
    from src.ui.cli_patient import run
    run()


def run_gradio():
    """Lance l'interface Gradio via subprocess."""
    import subprocess
    gradio_script = str(Path(__file__).parent / "src" / "ui" / "gradio_app.py")
    console.print("[dim]Lancement de l'interface Gradio...[/dim]")
    console.print("[bold green]Ouvrez votre navigateur sur : http://localhost:7860[/bold green]\n")
    console.print("[dim](Appuyez sur Ctrl+C pour arreter le serveur)[/dim]\n")
    subprocess.run([sys.executable, gradio_script])


def main():
    # Gestion des arguments CLI directs
    if "--cli" in sys.argv:
        run_cli()
        return
    if "--gradio" in sys.argv:
        run_gradio()
        return

    # Menu interactif
    display_banner()
    display_mode_menu()

    choice = Prompt.ask("[bold cyan]Votre choix[/bold cyan]", choices=["1", "2", "3"])

    if choice == "1":
        run_cli()
    elif choice == "2":
        run_gradio()
    else:
        console.print("\n[dim]Au revoir ![/dim]\n")


if __name__ == "__main__":
    main()
