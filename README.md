
# Generative AI & NLP Analytics Systems

This repository provides a complete reference implementation of a Generative AI and NLP Analytics system. 
It demonstrates Retrieval-Augmented Generation (RAG), LLM integration, distributed computing examples, 
and an end-to-end application with FastAPI backend and Streamlit frontend.

---

## Table of Contents

1. Introduction  
2. Features  
3. Architecture Overview  
4. Project Structure  
5. Installation  
6. Configuration  
7. Usage  
8. Distributed Computing Examples  
9. Testing  
10. Deployment Notes  
11. License  

---

## 1. Introduction

This project demonstrates how to build a production-style AI system that combines:

- Retrieval-Augmented Generation (RAG) pipelines for document-grounded answers.
- Integration with large language models (OpenAI API or HuggingFace fallback).
- WebSocket-based token streaming for real-time chat.
- Analytics assistants for finance and NLP tasks.
- Distributed training and data processing with Ray, Dask, and Spark.
- A lightweight Streamlit front-end for interactive use.

---

## 2. Features

- FastAPI backend (REST and WebSocket endpoints).
- RAG indexing using Sentence-Transformers and FAISS (with NumPy fallback).
- Configurable via `.env` file for API keys and embedding model choice.
- Support for both OpenAI API models and local HuggingFace models.
- Distributed examples: Ray tasks, Dask Bag, and Spark DataFrame word count.
- Streamlit-based client interface for ingestion and chat.
- PyTorch example for text classification.

---

## 3. Architecture Overview

1. **Data ingestion**: Documents are chunked and embedded into vector space.  
2. **Vector storage**: Embeddings are indexed using FAISS or NumPy.  
3. **Retriever**: Queries are embedded and top-k similar chunks retrieved.  
4. **Prompt builder**: Retrieved context is combined with user query.  
5. **LLM serving**: Response generated from OpenAI API or HuggingFace model.  
6. **Streaming**: FastAPI WebSocket streams partial responses to client.  
7. **Frontend**: Streamlit app provides a simple analytics assistant interface.

---

## 4. Project Structure

```
genai_nlp_analytics/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ app/
│  ├─ api.py
│  └─ ws_protocol.py
├─ rag/
│  ├─ ingest.py
│  ├─ retriever.py
│  ├─ vectorstore.py
│  ├─ embed.py
│  └─ prompt.py
├─ models/
│  └─ serving/
│      └─ llm.py
├─ clients/
│  ├─ cli.py
│  └─ streamlit_app.py
├─ data/
│  ├─ docs/
│  └─ finance/
└─ tests/
```

---

## 5. Installation

### Prerequisites
- Python 3.10 or higher
- pip and virtual environment support
- Optional: Docker (for containerized deployment)

### Steps

```bash
# Clone the repository
git clone <your-repo-url> genai_nlp_analytics
cd genai_nlp_analytics

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## 6. Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` to set variables:

- `OPENAI_API_KEY`: Optional, use OpenAI models if available.
- `OPENAI_MODEL`: Default is `gpt-4o-mini`.
- `USE_FAISS`: `1` (default) to use FAISS, `0` to fallback to NumPy.
- `EMBED_MODEL`: Embedding model, e.g., `sentence-transformers/all-MiniLM-L6-v2`.
- `CHUNK_SIZE`, `CHUNK_OVERLAP`: Controls for document chunking.
- `TOP_K`: Default retrieval size.

---

## 7. Usage

### Build the index
```bash
python -m rag.ingest --docs ./data/docs --index ./data/index --rebuild
```

### Start the backend
```bash
uvicorn app.api:app --reload --port 8000
```

Endpoints available:
- `GET /health` : Health check
- `POST /ingest` : Rebuild index
- `GET /search?query=...` : Retrieve chunks
- `POST /chat` : Get answer with context
- `WS /ws/stream` : Token streaming

### Use the Streamlit frontend
```bash
streamlit run clients/streamlit_app.py
```

### Command-line client
```bash
python clients/cli.py --q "What is RAG?" --index ./data/index
```

---

## 8. Distributed Computing Examples

### Ray
```bash
python distributed/ray_job.py
```

### Dask
```bash
python distributed/dask_job.py
```

### Spark
```bash
python distributed/spark_job.py
```

---

## 9. Testing

```bash
pytest -q
```

---

## 10. Deployment Notes

- **Docker**: A Dockerfile can be created based on `python:3.11-slim`.  
- Ensure system dependencies for FAISS and PyMuPDF are available.  
- Expose backend on port 8000 and Streamlit on port 8501.  
- For production, configure CORS, HTTPS, and reverse proxy (e.g., Nginx).  

---


## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m rag.ingest --docs ./data/docs --index ./data/index --rebuild
uvicorn app.api:app --reload --port 8000
streamlit run clients/streamlit_app.py
```


## 11. License

MIT License.  
Use freely for learning and prototyping. Attribution is appreciated.

