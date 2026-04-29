from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class FormatterInput(BaseModel):
    content: str = Field(description="Le texte brut à formater.")
    subject: str = Field(description="Le sujet de la fiche de synthèse.")

class FormatterTool(BaseTool):
    name: str = "markdown_formatter"
    description: str = "Formats raw medical text into a structured Markdown synthesis report (Executive Summary, Findings, Consensus, Divergences, Recommendations)."
    args_schema: Type[BaseModel] = FormatterInput
    
    def _run(self, content: str, subject: str) -> str:
        """(This tool is a dummy helper, realistically the WriterAgent uses prompt instructions, 
        but this ensures the structure constraint is enforced if the agent calls it.)"""
        
        # Ce tool force simplement l'agent à organiser ses idées
        # Souvent dans LangChain, on laisse l'agent générer du texte qu'on nettoie.
        # Ici c'est un utilitaire à disposition de l'agent.
        
        return (
            f"# Synthèse : {subject}\n\n"
            f"## Résumé exécutif\n\n"
            f"## Principales conclusions\n\n"
            f"## Points de consensus\n\n"
            f"## Points de divergence\n\n"
            f"## Recommandations\n\n"
            f"## Sources citées\n\n"
            f"--- Contenu brut (à intégrer) ---\n"
            f"{content[:500]}..."
        )

