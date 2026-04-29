import asyncio
from typing import Optional, Type, Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.rag.indexing import load_index
from src.rag.retrieval import create_query_engine, retrieve_context

class RAGInput(BaseModel):
    query: str = Field(description="La requête de recherche médicale.")

class RAGTool(BaseTool):
    name: str = "medical_knowledge_search"
    description: str = "Searches the indexed medical literature corpus for context and research papers based on the given query."
    args_schema: Type[BaseModel] = RAGInput
    
    # Instance as private variables
    _query_engine: Any = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize index
        try:
            index = load_index()
            # self._query_engine is not officially supported cleanly by BaseModel if it's not a field,
            # so we use object.__setattr__ to bypass pydantic checks for internal state on older pydantic if needed
            object.__setattr__(self, '_query_engine', create_query_engine(index))
        except Exception as e:
            print(f"Error initializing RAG Tool index: {e}")

    def _run(self, query: str) -> str:
        """Execute the search on the local index."""
        if not self._query_engine:
            return "Erreur: RAG query engine non initialisé ou index indisponible."
        
        return retrieve_context(query, self._query_engine)
        
    async def _arun(self, query: str) -> str:
        """Asynchronous execution."""
        return await asyncio.to_thread(self._run, query)

