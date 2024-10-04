from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSimilarityAnalyzer:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def compute_similarity(self, doc1, doc2):
        embeddings = self.model.encode([doc1, doc2])
        return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    def find_similar_documents(self, query_doc, corpus, top_n=5):
        query_embedding = self.model.encode([query_doc])[0]
        corpus_embeddings = self.model.encode(corpus)
        
        similarities = cosine_similarity([query_embedding], corpus_embeddings)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        return [
            {"document": corpus[i], "similarity": similarities[i]}
            for i in top_indices
        ]

# Uso:
# analyzer = SemanticSimilarityAnalyzer()
# similarity = analyzer.compute_similarity("The cat is on the mat", "There is a cat sitting on a mat")
# similar_docs = analyzer.find_similar_documents("AI in healthcare", ["AI applications in finance", "Machine learning in medicine", "Natural language processing advancements"])