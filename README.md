# MediSearch : Assistant de Veille Médicale Multi-Agents

MediSearch est un système d'intelligence artificielle conçu pour ingérer, indexer et synthétiser la littérature médicale de manière autonome. Ce projet repose sur un pipeline **RAG (LlamaIndex)** couplé à une orchestration de **4 agents spécialisés (LangChain / LangGraph)** pour automatiser la veille scientifique.

## Architecture du Système

```text
Orchestrateur (Séquentiel avec Gestion d'État)
├── 1. Agent Collecteur     → Recherche via RAG & Web (DuckDuckGo)
├── 2. Agent Analyste       → Analyse critique, consensus et contradictions
├── 3. Agent Rédacteur      → Mise en forme Markdown formatée
└── 4. Agent Validateur     → Contrôle qualité, score et auto-révision

Pipeline RAG (LlamaIndex)
├── Ingestion    : Fichiers locaux (PDF, TXT)
├── Chunking     : SentenceSplitter (512 tokens / 50 overlap)
├── Embeddings   : sentence-transformers/all-MiniLM-L6-v2 (Local, gratuit)
├── Vector Store : ChromaDB (Persistant)
└── LLM Base     : Ollama (llama3.2) local avec fallback API Groq (llama-3.1-8b)
```

## Choix Techniques
- **LangChain** a été choisi pour construire le réseau d'agents grâce au framework `create_react_agent` et à la facilité d'intégration d'outils personnalisés.
- **LlamaIndex** a été utilisé pour la partie RAG afin de rendre l'ingestion de formats complexes (PDF) et le requêtage extrêmement simple.
- **Ollama / Groq** : Support des environnements sans GPU via Groq API et fonctionnements hors-ligne 100% locaux via Ollama et Llama 3.2.

## Installation

### Prérequis
- Python 3.11+
- Ollama installé sur votre machine et le modèle Llama3.2 téléchargé (`ollama run llama3.2:1b`)

### Étapes
1. Cloner ce répertoire
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```
3. Copier `.env.example` vers `.env` et ajouter les valeurs requises (comme `GROQ_API_KEY` si désiré).

## Démarrage Rapide

1. **Générer les documents de test** et lancer l'indexation RAG :
```bash
python scripts/generate_sample_docs.py
python scripts/test_rag.py
```

2. **Lancer l'interface en ligne de commande (CLI)** :
```bash
python src/ui/cli.py
```

3. **(Optionnel) Lancer l'interface Web Gradio** :
```bash
python src/ui/gradio_app.py
```
Ouvrez votre navigateur sur `http://localhost:7860`.

## Exemple d'Utilisation

**Requête** : "Quels sont les effets des probiotiques sur l'immunité ?"

**Sortie attendue** : Un rapport Markdown structuré abordant :
- Résumé du rôle des probiotiques (Lactobacillus, Bifidobacterium).
- Points de consensus (réduction des infections respiratoires).
- Divergences (effets sur patients immunisés).
- Recommandations d'utilisation et sources citées.
