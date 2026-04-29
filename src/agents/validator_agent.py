from langchain_core.prompts import ChatPromptTemplate
import json

class ValidatorAgent:
    def __init__(self, llm, tools):
        # On s'assure d'avoir du texte en retour en ne liant pas d'outils
        self.llm = llm
    
    def validate(self, draft: str, raw_data: str) -> dict:
        prompt = f"""Tu es un relecteur scientifique rigoureux.
        Évalue la fiche de synthèse vis-à-vis des données brutes initiales.
        
        Données brutes : 
        {raw_data}
        
        Fiche de synthèse à valider : 
        {draft}
        
        Tu dois renvoyer STRICTEMENT ET UNIQUEMENT un objet JSON valide, sans aucun formatage Markdown autour, avec exactement ces 4 clés :
        {{
            "approved": true,
            "score": 85,
            "feedback": "ton commentaire d'amélioration court",
            "revised_draft": "une nouvelle version corrigée uniquement si le score est sous 70"
        }}
        """
        response = self.llm.invoke(prompt)
        content = str(response.content).strip()
        
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                return {
                    "approved": bool(data.get("approved", False)),
                    "score": int(data.get("score", 0)),
                    "feedback": str(data.get("feedback", "")),
                    "revised_draft": str(data.get("revised_draft", ""))
                }
            else:
                data = json.loads(content)
                return {
                    "approved": bool(data.get("approved", False)),
                    "score": int(data.get("score", 0)),
                    "feedback": str(data.get("feedback", "")),
                    "revised_draft": str(data.get("revised_draft", ""))
                }
        except Exception as e:
            return {
                "approved": False,
                "score": 0,
                "feedback": f"Erreur de parsing JSON du validateur: {str(e)}",
                "revised_draft": ""
            }
