import asyncio
from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun

class WebSearchInput(BaseModel):
    query: str = Field(description="La requête de recherche web.")

class WebSearchTool(BaseTool):
    name: str = "web_medical_search"
    description: str = "Searches the web for recent medical articles or terminology using DuckDuckGo."
    args_schema: Type[BaseModel] = WebSearchInput
    
    def _run(self, query: str) -> str:
        """Execute the duckduckgo search."""
        search = DuckDuckGoSearchRun()
        try:
            # On ajoute un context pour avoir des résultats médicaux
            medical_query = f"{query} medical research OR health"
            result = search.run(medical_query)
            return f"Résultats de recherche Web :\n{result}"
        except Exception as e:
            return f"Erreur lors de la recherche web: {str(e)}"
            
    async def _arun(self, query: str) -> str:
        return await asyncio.to_thread(self._run, query)

