# HackerRank Orchestrate - Support Triage Agent

This terminal-based AI agent triages support tickets for HackerRank, Claude, and Visa ecosystems using a Retrieval-Augmented Generation (RAG) approach.

## Setup Instructions

1. **Environment Setup:**
   - Ensure Python 3.9+ is installed.
   - Create a virtual environment: `python -m venv venv`
   - Activate it:
     - Windows: `.\venv\Scripts\activate`
     - Mac/Linux: `source venv/bin/activate`
   - Install dependencies: `pip install pandas langchain-openai langchain-huggingface langchain-community chromadb langchain-groq python-dotenv`

2. **API Keys:**
   - Create a `.env` file in the root directory.
   - Add your Groq API Key: `GROQ_API_KEY=your_key_here`

3. **Data Ingestion:**
   - Run `python ingest.py` to index the support corpus into the local vector database (`chroma_db`).

4. **Running the Agent:**
   - Run Ingestion: `python ingest.py` (This builds the brain inside code/chroma_db).
   - Run `python main.py` to process the tickets in `support_tickets/support_tickets.csv`.
   - Results will be saved to `support_tickets/output.csv`.

## Architecture
- **Retriever:** Uses `all-MiniLM-L6-v2` local embeddings via HuggingFace for cost-efficient, local data retrieval.
- **Brain:** Uses `llama-3.3-70b-versatile` via Groq for high-speed, grounded reasoning.
- **Triage Logic:** Strictly escalates high-risk cases (fraud, security, cheating) while replying to standard support queries.