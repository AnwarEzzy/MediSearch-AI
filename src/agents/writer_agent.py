from langchain_core.prompts import ChatPromptTemplate

class WriterAgent:
    def __init__(self, llm, tools):
        # On n'utilise pas bind_tools ici pour s'assurer que l'agent génère TOUJOURS
        # du texte pur et jamais d'objet tool_calls (JSON intrinsèque du LLM / LangChain).
        self.llm = llm
        
        # On extrait manuellement l'outil RAG s'il est présent dans la liste
        self.rag_tool = None
        for t in tools:
            if hasattr(t, "name") and t.name == "medical_knowledge_search":
                self.rag_tool = t
            elif type(t).__name__ == "RAGTool":
                self.rag_tool = t
    
    def write(self, analysis: str, query: str) -> str:
        # Appel explicite au RAG pour récupérer un contexte supplémentaire
        additional_context = ""
        if self.rag_tool:
            try:
                additional_context = self.rag_tool.invoke(query)
            except Exception as e:
                additional_context = f"(Erreur lors de l'appel au RAG: {e})"
        
        prompt = f"""Tu es un rédacteur médical scientifique vulgarisateur.
        Rédige une fiche de synthèse au format Markdown propre et professionnelle.
        NE RENVOIE AUCUN APPEL D'OUTIL ET AUCUN JSON. Ta réponse doit seulement être le texte Markdown.
        
        Sujet / Requête initiale : {query}
        Analyse de l'expert : {analysis}
        
        Contexte supplémentaire (RAG) :
        {additional_context}
        
        Ta réponse DOIT utiliser cette structure Markdown stricte :
        # Synthèse : {query}
        ## Résumé exécutif
        ## Principales conclusions
        ## Points de consensus
        ## Recommandations
        ## Sources citées
        """
        
        response = self.llm.invoke(prompt)
        return str(response.content)
