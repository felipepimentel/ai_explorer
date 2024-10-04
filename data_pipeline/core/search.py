from data_pipeline.processors.embedding import EmbeddingModel
from data_pipeline.processors.indexing import FaissIndex
import numpy as np

class DocumentSearch:
    def __init__(self, dimension=768):
        self.embedding_model = EmbeddingModel()
        self.vector_index = FaissIndex(dimension)

    def add_documents(self, documents, doc_type='text'):
        if doc_type == 'text':
            embeddings = [self.embedding_model.generate_text_embeddings(doc) for doc in documents]
        elif doc_type == 'pdf':
            embeddings = [self.embedding_model.generate_pdf_embeddings(doc) for doc in documents]
        elif doc_type == 'image':
            embeddings = [self.embedding_model.generate_image_embeddings(doc) for doc in documents]
        elif doc_type == 'audio':
            embeddings = [self.embedding_model.generate_audio_embeddings(doc) for doc in documents]
        else:
            raise ValueError(f"Unsupported document type: {doc_type}")

        self.vector_index.add_vectors(np.vstack(embeddings))

    def search_documents(self, query, k=3):
        query_embedding = self.embedding_model.generate_text_embeddings(query)
        distances, indices = self.vector_index.search(query_embedding, k)
        return distances, indices