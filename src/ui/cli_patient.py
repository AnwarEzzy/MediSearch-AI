import sys
import os
import json
from pathlib import Path


# Ensure project root is in path
sys.path.append(str(Path(__file__).parent.parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from src.orchestrator.patient_orchestrator import PatientOrchestrator

console = Console(highlight=False)

DB_PATH = Path(__file__).parent.parent.parent / "data" / "patients" / "patients_database.json"


def load_patients() -> list:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def display_header():
    console.print()
    console.print(Panel.fit(
        "[bold cyan]MediSearch -- Analyse Medicale des Patients[/bold cyan]\n"
        "[dim]Systeme multi-agents powered by Groq (Llama 3.1)[/dim]",
        border_style="cyan",
        padding=(1, 4)
    ))
    console.print()


def display_patients_table(patients: list):
    table = Table(
        title="Base de Donnees Patients",
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold blue",
        show_lines=True
    )
    table.add_column("ID",    style="bold yellow", width=4,  justify="center")
    table.add_column("Nom",   style="bold white",  width=22)
    table.add_column("Age",   justify="center",    width=5)
    table.add_column("Sexe",  justify="center",    width=5)
    table.add_column("Symptomes principaux", style="dim",     width=42)
    table.add_column("Antecedents",          style="red dim", width=25)

    for p in patients:
        symptoms   = ", ".join(p["symptomes"][:2]) + ("..." if len(p["symptomes"]) > 2 else "")
        antecedents = ", ".join(p["antecedents"][:2]) if p.get("antecedents") else "Aucun"
        table.add_row(str(p["id"]), p["nom"], str(p["age"]), p["sexe"], symptoms, antecedents)

    console.print(table)
    console.print()


def display_selection_menu():
    console.print(Panel(
        "[bold]OPTIONS DE SELECTION :[/bold]\n\n"
        "  [yellow][1][/yellow]  Un seul patient        [dim](ex: 5)[/dim]\n"
        "  [yellow][2][/yellow]  Plusieurs patients     [dim](ex: 1,3,7,12)[/dim]\n"
        "  [yellow][3][/yellow]  Plage de patients      [dim](ex: 5-15)[/dim]\n"
        "  [yellow][4][/yellow]  Tous les patients\n"
        "  [yellow][5][/yellow]  Recherche par nom      [dim](ex: Dupont)[/dim]\n"
        "  [yellow][6][/yellow]  Quitter",
        title="[bold cyan]Menu[/bold cyan]",
        border_style="cyan",
        padding=(0, 2)
    ))


def parse_selection(choice: str, option: str, patients: list) -> list:
    if option == "1":
        pid = int(choice.strip())
        return [p for p in patients if p["id"] == pid]
    elif option == "2":
        pids = [int(x.strip()) for x in choice.split(",")]
        return [p for p in patients if p["id"] in pids]
    elif option == "3":
        start, end = choice.strip().split("-")
        pids = list(range(int(start), int(end) + 1))
        return [p for p in patients if p["id"] in pids]
    elif option == "4":
        return patients
    elif option == "5":
        name = choice.strip().lower()
        return [p for p in patients if name in p["nom"].lower()]
    return []


def confirm_selection(selected: list) -> bool:
    table = Table(box=box.SIMPLE, border_style="green", header_style="bold green")
    table.add_column("ID",       width=4,  justify="center")
    table.add_column("Nom",      width=22)
    table.add_column("Age",      width=5,  justify="center")
    table.add_column("Symptomes", width=50)

    for p in selected:
        table.add_row(str(p["id"]), p["nom"], str(p["age"]), ", ".join(p["symptomes"]))

    console.print(f"\n[bold green]{len(selected)} patient(s) selectionne(s) :[/bold green]")
    console.print(table)
    answer = Prompt.ask("\n[bold]Lancer l'analyse ?[/bold]", choices=["o", "n"], default="o")
    return answer == "o"


def display_result(result: dict, index: int, total: int):
    patient = result["patient"]
    console.print()
    console.print(Panel(
        f"[bold cyan]Patient {index}/{total}[/bold cyan] -- [bold white]{patient['nom']}[/bold white]"
        f" | {patient['age']} ans | {patient['sexe']}\n"
        f"[dim]Symptomes : {', '.join(patient['symptomes'])}[/dim]",
        border_style="cyan"
    ))
    console.print(Markdown(result["diagnosis"]))
    console.print(f"\n[dim green]Fiche sauvegardee : {result['filepath']}[/dim green]")
    console.print("-" * 80)


def run():
    patients = load_patients()
    orchestrator = None

    while True:
        display_header()
        display_patients_table(patients)
        display_selection_menu()

        option = Prompt.ask(
            "\n[bold cyan]Votre choix[/bold cyan]",
            choices=["1", "2", "3", "4", "5", "6"]
        )

        if option == "6":
            console.print("\n[dim]Au revoir ![/dim]\n")
            break

        choice = ""
        if option == "1":
            choice = Prompt.ask("[bold]Entrez l'ID du patient[/bold]")
        elif option == "2":
            choice = Prompt.ask("[bold]Entrez les IDs separes par des virgules (ex: 1,3,7)[/bold]")
        elif option == "3":
            choice = Prompt.ask("[bold]Entrez la plage (ex: 5-15)[/bold]")
        elif option == "5":
            choice = Prompt.ask("[bold]Entrez le nom a rechercher[/bold]")

        try:
            selected = parse_selection(choice, option, patients)
        except Exception as e:
            console.print(f"[red]Saisie invalide : {e}[/red]")
            Prompt.ask("Appuyez sur Entree pour continuer")
            continue

        if not selected:
            console.print("[red]Aucun patient trouve avec cette selection.[/red]")
            Prompt.ask("Appuyez sur Entree pour continuer")
            continue

        if not confirm_selection(selected):
            console.print("[dim]Selection annulee.[/dim]")
            continue

        # Initialisation lazy de l'orchestrateur (Groq + RAG)
        if orchestrator is None:
            console.print("\n[dim]Initialisation du moteur Groq (Llama 3.1)...[/dim]")
            orchestrator = PatientOrchestrator()

        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[bold blue]{task.completed}/{task.total}[/bold blue]"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Analyse en cours...", total=len(selected))
            for patient in selected:
                progress.update(task, description=f"[cyan]Analyse : {patient['nom']}")
                result = orchestrator.analyze_patient(patient)
                results.append(result)
                progress.advance(task)

        console.print(f"\n[bold green]Analyse terminee ! {len(results)} fiche(s) generee(s).[/bold green]\n")

        for i, result in enumerate(results, 1):
            display_result(result, i, len(results))

        answer = Prompt.ask(
            "\n[bold]Effectuer une nouvelle analyse ?[/bold]",
            choices=["o", "n"],
            default="o"
        )
        if answer == "n":
            console.print("\n[dim]Au revoir ![/dim]\n")
            break


if __name__ == "__main__":
    run()
