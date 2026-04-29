from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

class CollectorAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.llm_with_tools = llm.bind_tools(tools)
    
    def collect(self, query: str) -> str:
        prompt = f"""Tu es un agent documentaliste de recherche (Collector).
        Ta mission est de collecter le maximum de données pertinentes pour la requête : "{query}"
        Utilise les outils RAG et de recherche Web à ta disposition.
        """
        # Exécution de l'agent qui invoquera les outils si nécessaire
        response = self.llm_with_tools.invoke(prompt)
        
        # En l'absence de boucle d'agent, si le modèle a simplement renvoyé un tool_call, on gère l'affichage.
        content = response.content
        if not content and hasattr(response, "tool_calls") and response.tool_calls:
            import json
            content = f"L'agent a invoqué les outils suivants : {json.dumps(response.tool_calls)}"
            
        return content
