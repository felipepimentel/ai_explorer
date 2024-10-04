import hashlib
import pickle
import os

class EmbeddingCache:
    def __init__(self, cache_dir='.embedding_cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_key(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text):
        key = self._get_cache_key(text)
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, text, embedding):
        key = self._get_cache_key(text)
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        with open(cache_file, 'wb') as f:
            pickle.dump(embedding, f)

# Uso:
# cache = EmbeddingCache()
# embedding = cache.get(text)
# if embedding is None:
#     embedding = generate_embedding(text)
#     cache.set(text, embedding)