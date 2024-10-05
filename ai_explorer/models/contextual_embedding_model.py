from transformers import BertModel, BertTokenizer
import torch
from models.base_embedding_model import BaseEmbeddingModel
import threading

class ContextualEmbeddingModel(BaseEmbeddingModel):
    _tokenizer = None
    _model = None
    _lock = threading.Lock()

    def __init__(self):
        with ContextualEmbeddingModel._lock:
            if ContextualEmbeddingModel._tokenizer is None:
                ContextualEmbeddingModel._tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
            if ContextualEmbeddingModel._model is None:
                ContextualEmbeddingModel._model = BertModel.from_pretrained("bert-base-uncased")
        self.tokenizer = ContextualEmbeddingModel._tokenizer
        self.model = ContextualEmbeddingModel._model

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
