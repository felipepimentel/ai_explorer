from sklearn.cluster import KMeans
from data_pipeline.processors.embedding import EmbeddingModel

class DocumentClusterer:
    def __init__(self, n_clusters=5):
        self.embedder = EmbeddingModel()
        self.kmeans = KMeans(n_clusters=n_clusters)

    def cluster_documents(self, documents):
        embeddings = [self.embedder.generate_text_embeddings(doc) for doc in documents]
        clusters = self.kmeans.fit_predict(embeddings)
        return clusters

    def get_cluster_centers(self):
        return self.kmeans.cluster_centers_

    def assign_cluster(self, document):
        embedding = self.embedder.generate_text_embeddings(document)
        return self.kmeans.predict([embedding])[0]

# Uso:
# clusterer = DocumentClusterer(n_clusters=10)
# clusters = clusterer.cluster_documents(["doc1", "doc2", "doc3"])
# new_doc_cluster = clusterer.assign_cluster("new document")