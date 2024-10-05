import hashlib
import shelve

import numpy as np
import PyPDF2
import pytesseract
import whisper
from cachetools import TTLCache, cached
from PIL import Image
from sentence_transformers import SentenceTransformer
from transformers import (
    DistilBertModel,
    DistilBertTokenizer,
)

from .config import Config
from .models import FileType


class EmbeddingModel:
    def __init__(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            "distilbert-base-multilingual-cased"
        )
        self.model = DistilBertModel.from_pretrained(
            "distilbert-base-multilingual-cased"
        )
        self.whisper_model = whisper.load_model("base")
        self.sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

    @cached(cache=TTLCache(maxsize=100, ttl=Config.CACHE_EXPIRATION_TIME))
    def generate_embeddings(self, text: str) -> np.array:
        return self.sentence_transformer.encode(text)

    def generate_pdf_embeddings(self, filepath: str) -> np.array:
        pdf_reader = PyPDF2.PdfReader(filepath)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()
        return self.generate_embeddings(content)

    def generate_image_embeddings(self, filepath: str) -> np.array:
        img = Image.open(filepath)
        content = pytesseract.image_to_string(img)
        return self.generate_embeddings(content)

    def generate_audio_embeddings(self, filepath: str) -> np.array:
        transcription = self.whisper_model.transcribe(filepath)
        return self.generate_embeddings(transcription["text"])


class EmbeddingService:
    def __init__(self):
        self.model = EmbeddingModel()
        self.persistent_cache = shelve.open(Config.PERSISTENT_CACHE_PATH)

    def embed(self, data: str, data_type: FileType) -> np.array:
        cache_key = f"{data_type.value}:{hashlib.md5(data.encode()).hexdigest()}"
        if cache_key in self.persistent_cache:
            return self.persistent_cache[cache_key]

        if data_type == FileType.TEXT:
            embedding = self.model.generate_embeddings(data)
        elif data_type == FileType.PDF:
            embedding = self.model.generate_pdf_embeddings(data)
        elif data_type == FileType.IMAGE:
            embedding = self.model.generate_image_embeddings(data)
        elif data_type == FileType.AUDIO:
            embedding = self.model.generate_audio_embeddings(data)
        else:
            raise ValueError(f"Unsupported data type for embedding: {data_type}")

        self.persistent_cache[cache_key] = embedding
        return embedding

    def close(self):
        self.persistent_cache.close()
