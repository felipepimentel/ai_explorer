from models.base_embedding_model import BaseEmbeddingModel
import numpy as np

class EmbeddingModel(BaseEmbeddingModel):
    def embed(self, text):
        # Placeholder for actual embedding logic
        return np.random.rand(768)
