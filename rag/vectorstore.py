import os, pickle, pathlib, numpy as np
USE_FAISS = os.getenv("USE_FAISS", "1") == "1"
if USE_FAISS:
    try:
        import faiss
    except Exception:
        USE_FAISS = False

def save_index(index_dir, embeddings, metadatas):
    p = pathlib.Path(index_dir)
    p.mkdir(parents=True, exist_ok=True)
    if USE_FAISS:
        import faiss
        idx = faiss.IndexFlatIP(embeddings.shape[1])
        idx.add(embeddings.astype("float32"))
        faiss.write_index(idx, str(p/"index.faiss"))
    else:
        np.save(p/"vectors.npy", embeddings)
    pickle.dump(metadatas, open(p/"meta.pkl","wb"))

def load_index(index_dir):
    p = pathlib.Path(index_dir)
    metas = pickle.load(open(p/"meta.pkl","rb"))
    if USE_FAISS and (p/"index.faiss").exists():
        import faiss
        idx = faiss.read_index(str(p/"index.faiss"))
        return ("faiss", idx, metas)
    else:
        vecs = np.load(p/"vectors.npy")
        return ("numpy", vecs, metas)
