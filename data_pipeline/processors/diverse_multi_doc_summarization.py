from transformers import pipeline
from sklearn.cluster import KMeans
from data_pipeline.processors.embedding import EmbeddingModel

class DiverseMultiDocSummarizer:
    def __init__(self, num_clusters=3):
        self.summarizer = pipeline("summarization")
        self.embedder = EmbeddingModel()
        self.num_clusters = num_clusters

    def summarize(self, documents, max_length=150):
        embeddings = np.array([self.embedder.generate_text_embeddings(doc) for doc in documents])
        
        kmeans = KMeans(n_clusters=self.num_clusters)
        clusters = kmeans.fit_predict(embeddings)
        
        cluster_summaries = []
        for i in range(self.num_clusters):
            cluster_docs = [doc for doc, cluster in zip(documents, clusters) if cluster == i]
            if cluster_docs:
                cluster_text = " ".join(cluster_docs)
                summary = self.summarizer(cluster_text, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
                cluster_summaries.append(summary)
        
        return cluster_summaries

# Uso:
# summarizer = DiverseMultiDocSummarizer()
# summaries = summarizer.summarize(["Doc1", "Doc2", "Doc3", "Doc4", "Doc5"])