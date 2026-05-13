import sys
import os
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv

# Charger le .env AVANT tout import qui utilise os.getenv()
_root = Path(__file__).parent.parent.parent
load_dotenv(dotenv_path=_root / ".env")

sys.path.append(str(_root))

from src.orchestrator.orchestrator import get_llm
from src.agents.collector_agent import CollectorAgent
from src.agents.analyst_agent import AnalystAgent
from src.agents.writer_agent import WriterAgent
from src.agents.validator_agent import ValidatorAgent
from src.tools.rag_tool import RAGTool
from src.tools.web_search_tool import WebSearchTool
from src.tools.formatter_tool import FormatterTool


def process_query_stream(query):
    if not query.strip():
        yield ("⚠️ Veuillez entrer une requête.", "", "", None)
        return

    # Valeurs par défaut pour chaque yield
    status = "⚙️ Initialisation du modèle (chargement des LLMs)..."
    report = ""
    score_display = ""
    file_path = None
    yield (status, report, score_display, file_path)

    llm = get_llm()
    rag_tool = RAGTool()
    web_tool = WebSearchTool()
    formatter_tool = FormatterTool()

    collector = CollectorAgent(llm, [rag_tool, web_tool])
    analyst = AnalystAgent(llm, [rag_tool])
    writer = WriterAgent(llm, [rag_tool, formatter_tool])
    validator = ValidatorAgent(llm, [])

    status += "\n🔍 Étape 1 : Collecte des données en cours..."
    yield (status, report, score_display, file_path)

    collected_data = collector.collect(query)

    status += "\n✅ Collecte terminée.\n🧠 Étape 2 : Analyse en cours..."
    yield (status, report, score_display, file_path)

    analysis = analyst.analyze(collected_data, query)

    status += "\n✅ Analyse terminée.\n✍️ Étape 3 : Rédaction en cours..."
    yield (status, report, score_display, file_path)

    draft = writer.write(analysis, query)
    report = draft

    status += "\n✅ Rédaction terminée.\n✅ Étape 4 : Validation en cours..."
    yield (status, report, score_display, file_path)

    validation_result = validator.validate(draft, collected_data)

    is_approved = validation_result.get("approved", False)
    score = validation_result.get("score", 0)
    feedback = validation_result.get("feedback", "Aucun feedback")
    revised = validation_result.get("revised_draft", "")

    final_report = draft
    if not is_approved and revised and len(revised) > 50:
        status += "\n🔄 Révision suite au retour du validateur..."
        final_report = revised

    status += "\n🎉 Processus complet terminé !"

    if is_approved:
        score_display = f"✅ {score}/100 — Approuvé\nFeedback : {feedback}"
    else:
        score_display = f"❌ {score}/100 — Révision nécessaire\nFeedback : {feedback}"

    # Sauvegarde du rapport
    os.makedirs("outputs", exist_ok=True)
    file_path = os.path.abspath("outputs/rapport_temp.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_report)

    yield (status, final_report, score_display, file_path)


with gr.Blocks(title="MediSearch AI") as demo:
    gr.Markdown("# 🏥 MediSearch - Assistant de Veille Médicale")
    gr.Markdown("Posez votre question médicale. Le système orchestre 4 agents (Collecteur, Analyste, Rédacteur, Validateur) pour vous fournir une synthèse.")

    with gr.Row():
        with gr.Column(scale=1):
            query_input = gr.Textbox(
                label="Votre requête",
                placeholder="Quels sont les effets des probiotiques sur l'immunité ?",
                lines=2
            )
            submit_btn = gr.Button("Lancer la recherche", variant="primary")
            status_box = gr.Textbox(label="Statut du Workflow", lines=8, interactive=False)
            score_box = gr.Textbox(label="Score de Validation", interactive=False, lines=3)
            download_file = gr.File(label="Télécharger le rapport (.md)")

        with gr.Column(scale=2):
            report_output = gr.Markdown(label="Fiche de Synthèse Générée")

    submit_btn.click(
        fn=process_query_stream,
        inputs=[query_input],
        outputs=[status_box, report_output, score_box, download_file]
    )

if __name__ == "__main__":
    print("Demarrage de l'interface Gradio...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=None,   # Gradio trouve automatiquement un port libre
        share=False,
        theme=gr.themes.Soft()
    )
