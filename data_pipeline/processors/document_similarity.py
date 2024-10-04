from sklearn.metrics.pairwise import cosine_similarity
from data_pipeline.processors.contextual_embeddings import ContextualEmbedder

class DocumentSimilarityAnalyzer:
    def __init__(self):
        self.embedder = ContextualEmbedder()

    def compute_similarity(self, doc1, doc2):
        emb1 = self.embedder.generate_embedding(doc1)
        emb2 = self.embedder.generate_embedding(doc2)
        return cosine_similarity([emb1], [emb2])[0][0]

    def find_similar_documents(self, query_doc, corpus, top_n=5):
        query_emb = self.embedder.generate_embedding(query_doc)
        corpus_embs = self.embedder.generate_batch_embeddings(corpus)
        similarities = cosine_similarity([query_emb], corpus_embs)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        return [(corpus[i], similarities[i]) for i in top_indices]

# Uso:
# analyzer = DocumentSimilarityAnalyzer()
# similarity = analyzer.compute_similarity("Doc1 content", "Doc2 content")
# similar_docs = analyzer.find_similar_documents("Query doc", ["Doc1", "Doc2", "Doc3"])