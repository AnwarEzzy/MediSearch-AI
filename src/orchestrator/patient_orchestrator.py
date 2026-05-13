import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.agents.patient_analyst_agent import PatientAnalystAgent
from src.tools.rag_tool import RAGTool

load_dotenv()


def get_groq_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0
    )


class PatientOrchestrator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.analyst = PatientAnalystAgent(self.llm)
        try:
            self.rag_tool = RAGTool()
        except Exception:
            self.rag_tool = None

    def _get_rag_context(self, patient: dict) -> str:
        """Récupère le contexte RAG à partir des symptômes du patient."""
        if not self.rag_tool:
            return ""
        symptoms_query = ", ".join(patient.get("symptomes", []))
        try:
            return self.rag_tool.invoke(symptoms_query)
        except Exception:
            return ""

    def analyze_patient(self, patient: dict) -> dict:
        """Pipeline complet d'analyse pour un patient."""
        rag_context = self._get_rag_context(patient)
        diagnosis = self.analyst.analyze(patient, rag_context)

        # Sauvegarde
        output_dir = os.path.join("outputs", "patients")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"patient_{patient['id']}_{patient['nom'].replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)

        header = (
            f"# Fiche Médicale — {patient['nom']}\n"
            f"**Date d'analyse :** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"**Âge :** {patient['age']} ans | **Sexe :** {patient['sexe']}\n\n"
            f"**Symptômes :** {', '.join(patient.get('symptomes', []))}\n\n---\n\n"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + diagnosis)

        return {
            "patient": patient,
            "diagnosis": diagnosis,
            "filepath": filepath
        }
