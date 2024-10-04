import faiss
import numpy as np

class FaissIndex:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add_vectors(self, vectors):
        self.index.add(np.array(vectors).astype('float32'))

    def search(self, query_vector, k=5):
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), k)
        return distances[0], indices[0]

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = FaissIndex(dimension)
    index.add_vectors(embeddings)
    return index