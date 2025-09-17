# Generative AI & NLP Analytics Systems

This project is a **reference implementation** of:
- Retrieval-Augmented Generation (RAG) pipelines
- Generative AI assistants with FastAPI backend (REST + WebSockets)
- LLM serving (OpenAI or local HuggingFace fallback)
- Distributed processing examples (Ray, Dask, Spark)
- Streamlit analytics UI
- Toy PyTorch classifier demo
- Financial sentiment mini-analysis

## Project structure
See code layout inside the repo.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m rag.ingest --docs ./data/docs --index ./data/index --rebuild
uvicorn app.api:app --reload --port 8000
streamlit run clients/streamlit_app.py
```
