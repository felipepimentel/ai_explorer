from processing.chunking import chunk_file
from processing.embedding import generate_embeddings
from processing.normalization import normalize_embeddings
from utils.cache import cache_embeddings

class ProcessingService:
    def process_file(self, file_path):
        file_chunks = chunk_file(file_path)
        embeddings = generate_embeddings(file_chunks)
        normalized_embeddings = normalize_embeddings(embeddings)
        cache_embeddings(file_path, normalized_embeddings)
