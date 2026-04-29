import os
from rich.console import Console
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

from src.agents.collector_agent import CollectorAgent
from src.agents.analyst_agent import AnalystAgent
from src.agents.writer_agent import WriterAgent
from src.agents.validator_agent import ValidatorAgent
from src.tools.rag_tool import RAGTool
from src.tools.web_search_tool import WebSearchTool
from src.tools.formatter_tool import FormatterTool

console = Console()

def get_llm():
    if os.getenv("GROQ_API_KEY"):
        return ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2:1b"), temperature=0)

class MediSearchOrchestrator:
    def __init__(self):
        console.print("[dim]Initialisation des agents (chargement des LLMs)...[/dim]")
        self.llm = get_llm()
        
        self.collector = CollectorAgent(self.llm, [RAGTool(), WebSearchTool()])
        self.analyst = AnalystAgent(self.llm, [RAGTool()])
        self.writer = WriterAgent(self.llm, [FormatterTool()])
        self.validator = ValidatorAgent(self.llm, [])
        self.shared_state = {}

    def run(self, query: str) -> dict:
        self.shared_state = {"query": query}
        
        # 1. Collecte
        console.print("\n[bold blue]ðŸ” Collecte en cours... [Agent Collecteur][/bold blue]")
        collected_data = self.collector.collect(query)
        self.shared_state["collected_data"] = collected_data
        
        source_count = collected_data.lower().count("source:") or 1
        console.print(f"   [green]â†’ Passages pertinents trouvÃ©s avec ~{source_count} sources.[/green]")
        
        # 2. Analyse
        console.print("\n[bold blue]ðŸ§  Analyse en cours... [Agent Analyste][/bold blue]")
        analysis = self.analyst.analyze(collected_data, query)
        self.shared_state["analysis"] = analysis
        console.print(f"   [green]â†’ Tendances, consensus et divergences identifiÃ©s.[/green]")
        
        # 3. RÃ©daction
        console.print("\n[bold blue]âœï¸ RÃ©daction en cours... [Agent RÃ©dacteur][/bold blue]")
        draft = self.writer.write(analysis, query)
        self.shared_state["draft"] = draft
        words = len(draft.split())
        console.print(f"   [green]â†’ Fiche de ~{words} mots gÃ©nÃ©rÃ©e.[/green]")
        
        # 4. Validation
        console.print("\n[bold blue]âœ… Validation en cours... [Agent Validateur][/bold blue]")
        validation_result = self.validator.validate(draft, collected_data)
        
        is_approved = validation_result.get("approved", False)
        score = validation_result.get("score", 0)
        feedback = validation_result.get("feedback", "Aucun feedback")
        
        if is_approved:
            console.print(f"   [green]â†’ Score qualitÃ© : {score}/100 â€” ApprouvÃ©[/green]")
        else:
            console.print(f"   [red]â†’ Score qualitÃ© : {score}/100 â€” RefusÃ©[/red]")
            console.print(f"   [yellow]ðŸ”„ RÃ©vision requise: {feedback}[/yellow]")
            revised = validation_result.get("revised_draft", "")
            if revised and len(revised) > 50:
                 self.shared_state["draft"] = revised
                 console.print("   [green]â†’ Draft rÃ©visÃ© appliquÃ©.[/green]")
        
        return {
            "query": query,
            "final_report": self.shared_state["draft"],
            "validation_score": score,
            "validation_feedback": feedback,
            "sources_count": source_count
        }

