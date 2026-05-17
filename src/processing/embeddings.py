import numpy as np
from sentence_transformers import SentenceTransformer   

_model = None

def get_embedding(text:str):
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    if not text or not text.strip():
        return None
    embedding=_model.encode(text,normalize_embeddings=True)
    return embedding