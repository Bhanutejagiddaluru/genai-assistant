import os, glob, pathlib, re, numpy as np
from .embed import embed_texts
from .vectorstore import save_index, load_index

def chunk_text(text, chunk_size=800, overlap=120):
    tokens = re.split(r'(\s+)', text)
    chunks, current, length = [], [], 0
    for t in tokens:
        current.append(t)
        length += len(t)
        if length >= chunk_size:
            chunks.append("".join(current))
            tail = "".join(current)[-overlap:]
            current = [tail]; length = len(tail)
    if current: chunks.append("".join(current))
    return [c.strip() for c in chunks if c.strip()]

def build_corpus(docs_dir):
    paths = []
    for ext in ("*.md","*.txt"):
        paths.extend(glob.glob(str(pathlib.Path(docs_dir)/ext)))
    texts, metas = [], []
    for path in paths:
        raw = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")
        for ch in chunk_text(raw):
            texts.append(ch); metas.append({"source": path})
    return texts, metas

def build_index(docs_dir, index_dir):
    texts, metas = build_corpus(docs_dir)
    embs = embed_texts(texts)
    save_index(index_dir, embs, [{"text":t, **m} for t,m in zip(texts, metas)])
    return index_dir

class Retriever:
    def __init__(self, index_dir):
        self.kind, self.index, self.metas = load_index(index_dir)
    def search(self, query, top_k=4):
        qvec = embed_texts([query])[0]
        if self.kind=="faiss":
            import faiss
            D,I = self.index.search(qvec.reshape(1,-1).astype("float32"), top_k)
            return [self.metas[i] for i in I[0]]
        else:
            sims = self.index @ qvec.reshape(-1,1)
            idx = np.argsort(-sims.flatten())[:top_k]
            return [self.metas[i] for i in idx]
