import os
from sentence_transformers import SentenceTransformer

_model = None
def get_embed_model():
    global _model
    if _model is None:
        model_name = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _model = SentenceTransformer(model_name)
    return _model

def embed_texts(texts):
    return get_embed_model().encode(texts, convert_to_numpy=True, normalize_embeddings=True)
