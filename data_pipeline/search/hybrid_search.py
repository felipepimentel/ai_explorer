from data_pipeline.utils.semantic_search import perform_semantic_search
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class HybridSearch:
    def __init__(self, documents):
        self.documents = documents
        self.tfidf = TfidfVectorizer().fit(documents)
        self.tfidf_matrix = self.tfidf.transform(documents)

    def keyword_search(self, query, k=5):
        query_vec = self.tfidf.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_k = similarities.argsort()[-k:][::-1]
        return [(self.documents[i], similarities[i]) for i in top_k]

    def semantic_search(self, query, k=5):
        return perform_semantic_search(self.documents, query, k)

    def hybrid_search(self, query, k=5, alpha=0.5):
        keyword_results = self.keyword_search(query, k)
        semantic_results = self.semantic_search(query, k)
        
        combined_results = {}
        for doc, score in keyword_results + semantic_results:
            if doc in combined_results:
                combined_results[doc] += score * alpha
            else:
                combined_results[doc] = score * (1 - alpha)
        
        sorted_results = sorted(combined_results.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:k]

# Uso:
# searcher = HybridSearch(["doc1", "doc2", "doc3"])
# results = searcher.hybrid_search("query", k=5, alpha=0.7)