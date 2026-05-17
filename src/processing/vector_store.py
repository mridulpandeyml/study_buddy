import faiss
import numpy as np
import os
from src.processing.embeddings import get_embedding

class VectorStore:
    def __init__(self, index_path="data/faiss_index.bin"):
        self.index_path = index_path
        self.dimension = 384  # MiniLM-L6-v2 output dimension
        self.index = None
        self.chunks = []
        self._load_or_create_index()

    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
            except Exception as e:
                print(f"Error loading FAISS index: {e}")
                self.index = faiss.IndexFlatL2(self.dimension)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def add_chunks(self, chunks):
        """Embeds and adds chunks to the FAISS index."""
        if not chunks:
            return
        
        embeddings = []
        valid_chunks = []
        for chunk in chunks:
            emb = get_embedding(chunk)
            if emb is not None:
                embeddings.append(emb)
                valid_chunks.append(chunk)
                
        if embeddings:
            embeddings_np = np.array(embeddings).astype('float32')
            self.index.add(embeddings_np)
            self.chunks.extend(valid_chunks)
            # We would typically save chunk texts to a JSON or DB here.
            # For simplicity, we just keep them in memory.
            faiss.write_index(self.index, self.index_path)

    def search(self, query, top_k=3):
        """Searches the vector store for top_k relevant chunks."""
        if not self.chunks or self.index.ntotal == 0:
            return []
            
        query_emb = get_embedding(query)
        if query_emb is None:
            return []
            
        query_np = np.array([query_emb]).astype('float32')
        distances, indices = self.index.search(query_np, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results
