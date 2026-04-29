# MediSearch: Multi-Agent Medical Literature Assistant

MediSearch is an AI system designed to autonomously ingest, index, and synthesize 
medical literature. It combines a **RAG pipeline (LlamaIndex)** with an orchestration 
of **4 specialized agents (LangChain)** to automate scientific monitoring and 
generate structured research reports.

## System Architecture

Orchestrator (Sequential with Shared State Management)
├── 1. Collector Agent   → Retrieves relevant passages via RAG & Web (DuckDuckGo)
├── 2. Analyst Agent     → Critical analysis, consensus detection & contradictions
├── 3. Writer Agent      → Generates structured Markdown synthesis report
└── 4. Validator Agent   → Quality control, scoring & auto-revision

RAG Pipeline (LlamaIndex)
├── Ingestion    : Local files (PDF, TXT)
├── Chunking     : SentenceSplitter (512 tokens / 50 overlap)
├── Embeddings   : sentence-transformers/all-MiniLM-L6-v2 (Local, free)
├── Vector Store : ChromaDB (Persistent)
└── LLM          : Ollama (llama3.2:1b) local + fallback Groq API (llama-3.1-8b)

## Technical Choices

- **LangChain** was chosen to build the agent network using the `create_react_agent` 
  framework and its seamless integration of custom tools.
- **LlamaIndex** handles the RAG pipeline, making document ingestion (PDF, TXT) 
  and semantic querying straightforward and efficient.
- **Ollama / Groq** : Supports GPU-free environments via the Groq API, 
  and fully offline local execution via Ollama with Llama 3.2.

## Installation

### Prerequisites
- Python 3.11+
- Ollama installed on your machine with the Llama 3.2 model pulled:
  ollama pull llama3.2:1b

### Steps

1. Clone this repository
2. Install dependencies:
   pip install -r requirements.txt
3. Copy `.env.example` to `.env` and fill in the required values 
   (e.g. GROQ_API_KEY if desired)

## Quick Start

1. Generate sample documents and build the RAG index:
   python scripts/generate_sample_docs.py
   python scripts/test_rag.py

2. Launch the CLI interface:
   python src/ui/cli.py

3. (Optional) Launch the Gradio web interface:
   python src/ui/gradio_app.py
   Then open your browser at http://localhost:7860

## Usage Example

**Query**: "What are the effects of probiotics on the immune system?"

**Expected output**: A structured Markdown report covering:
- Summary of probiotic roles (Lactobacillus, Bifidobacterium)
- Consensus points (reduction of respiratory infections)
- Divergences (effects on immunocompromised patients)
- Usage recommendations and cited sources

## Tech Stack

| Technology | Role |
|---|---|
| LangChain | Agent development, tools, orchestration |
| LlamaIndex | RAG pipeline, document indexing, retrieval |
| Ollama | Local LLM inference (llama3.2:1b) |
| Groq API | Cloud LLM fallback (llama-3.1-8b-instant) |
| ChromaDB | Persistent vector store |
| HuggingFace | Sentence embeddings (all-MiniLM-L6-v2) |
| Gradio | Web user interface |
| Rich | CLI interface |
| Python 3.11+ | Core language |

## Project Structure

medisearch/
├── data/raw/              # Source documents (PDF, TXT)
├── vectorstore/           # ChromaDB persistent index (gitignored)
├── src/
│   ├── config.py          # Centralized settings
│   ├── rag/               # Ingestion, indexing, retrieval
│   ├── agents/            # 4 specialized agents
│   ├── tools/             # RAG tool, web search, formatter
│   ├── orchestrator/      # Sequential workflow orchestration
│   └── ui/                # CLI and Gradio interfaces
├── scripts/               # Standalone utility scripts
├── outputs/               # Generated reports (.md)
├── .env.example
├── requirements.txt
└── README.md
