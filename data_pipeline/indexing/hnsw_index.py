import hnswlib
import numpy as np

class HNSWIndex:
    def __init__(self, dim, max_elements):
        self.index = hnswlib.Index(space='cosine', dim=dim)
        self.index.init_index(max_elements=max_elements, ef_construction=200, M=16)
        self.index.set_ef(50)
        self.current_id = 0
        self.id_to_doc = {}

    def add_item(self, vector, doc_id):
        self.index.add_items(vector, [self.current_id])
        self.id_to_doc[self.current_id] = doc_id
        self.current_id += 1

    def search(self, query_vector, k=5):
        labels, distances = self.index.knn_query(query_vector, k)
        return [(self.id_to_doc[label], dist) for label, dist in zip(labels[0], distances[0])]

    def save(self, file_path):
        self.index.save_index(file_path)

    def load(self, file_path):
        self.index.load_index(file_path)

# Uso:
# index = HNSWIndex(dim=768, max_elements=100000)
# index.add_item(embedding, doc_id)
# results = index.search(query_embedding)