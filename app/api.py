import os, json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from rag.retriever import Retriever
from rag.prompt import build_prompt
from models.serving.llm import get_llm
from app.ws_protocol import stream_tokens

load_dotenv()
app = FastAPI(title="GenAI & NLP Analytics API")

class IngestRequest(BaseModel):
    docs_dir: str = "./data/docs"
    index_dir: str = "./data/index"
    rebuild: bool = True

class ChatRequest(BaseModel):
    question: str
    index_dir: str = "./data/index"
    top_k: int = int(os.getenv("TOP_K", 4))

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ingest")
def ingest(req: IngestRequest):
    from rag.ingest import build_or_update_index
    index_path = build_or_update_index(req.docs_dir, req.index_dir, rebuild=req.rebuild)
    return {"status": "ok", "index": index_path}

@app.get("/search")
def search(q: str = Query(..., alias="query"), index_dir: str = "./data/index", k: int = 4):
    retr = Retriever(index_dir)
    results = retr.search(q, top_k=k)
    return {"query": q, "results": results}

@app.post("/chat")
def chat(req: ChatRequest):
    retr = Retriever(req.index_dir)
    ctx = retr.search(req.question, top_k=req.top_k)
    context_text = "\n\n".join([c["text"] for c in ctx])
    prompt = build_prompt(req.question, context_text)
    llm = get_llm()
    answer = llm.generate(prompt)
    return JSONResponse({"answer": answer, "context": ctx})

@app.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            payload = json.loads(raw)
            q = payload.get("question", "")
            index_dir = payload.get("index_dir", "./data/index")
            top_k = int(payload.get("top_k", os.getenv("TOP_K", 4)))

            retr = Retriever(index_dir)
            ctx = retr.search(q, top_k=top_k)
            context_text = "\n\n".join([c["text"] for c in ctx])
            prompt = build_prompt(q, context_text)
            llm = get_llm()
            full = llm.generate(prompt)

            async for chunk in stream_tokens(full):
                await ws.send_text(chunk)
            await ws.send_text("[[END]]")
    except WebSocketDisconnect:
        return
