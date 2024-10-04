from sentence_transformers import SentenceTransformer

class DocumentEmbedder:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_document(self, document):
        return self.model.encode(document)

    def embed_documents(self, documents):
        return self.model.encode(documents)

# Uso:
# embedder = DocumentEmbedder()
# embedding = embedder.embed_document("This is a sample document.")
# embeddings = embedder.embed_documents(["Doc1", "Doc2", "Doc3"])