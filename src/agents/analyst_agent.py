from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

class AnalystAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.llm_with_tools = llm.bind_tools(tools)
    
    def analyze(self, collected_data: str, query: str) -> str:
        prompt = f"""Tu es un analyste médical expert.
        Compare et analyse les données brutes suivantes pour répondre à la requête initiale : "{query}"
        
        Données collectées :
        {collected_data}
        
        Dresse un bilan structuré mettant en évidence :
        1. Les points de consensus
        2. Les contradictions ou divergences
        3. Les lacunes dans les données
        """
        response = self.llm_with_tools.invoke(prompt)
        
        content = response.content
        if not content and hasattr(response, "tool_calls") and response.tool_calls:
            import json
            content = f"L'agent a invoqué les outils suivants : {json.dumps(response.tool_calls)}"
            
        return content
