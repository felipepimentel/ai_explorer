from models.embedding_model import EmbeddingModel
from models.contextual_embedding_model import ContextualEmbeddingModel
from models.base_embedding_model import BaseEmbeddingModel

class HybridEmbeddingModel(BaseEmbeddingModel):
    def __init__(self):
        self.base_model = EmbeddingModel()
        self.contextual_model = ContextualEmbeddingModel()

    def embed(self, text):
        base_embedding = self.base_model.embed(text)
        contextual_embedding = self.contextual_model.embed(text)
        return 0.5 * base_embedding + 0.5 * contextual_embedding
