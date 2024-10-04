import numpy as np
from data_pipeline.processors.embedding import Embedder
from data_pipeline.processors.indexing import FaissIndex

class SemanticSearch:
    def __init__(self, texts, embedder=None):
        self.texts = texts
        self.embedder = embedder or Embedder()
        self.embeddings = np.array([self.embedder.generate_embedding(text) for text in texts])
        self.index = FaissIndex(self.embeddings.shape[1])
        self.index.add_vectors(self.embeddings)

    def search(self, query, k=5):
        query_embedding = self.embedder.generate_embedding(query)
        distances, indices = self.index.search(query_embedding, k)
        results = [
            {"text": self.texts[i], "score": 1 - dist / 2}  # Normalize distance to similarity score
            for i, dist in zip(indices, distances)
        ]
        return sorted(results, key=lambda x: x["score"], reverse=True)

def perform_semantic_search(texts, query, k=5):
    searcher = SemanticSearch(texts)
    return searcher.search(query, k)