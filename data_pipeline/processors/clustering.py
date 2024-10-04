from sklearn.cluster import KMeans
import numpy as np

def cluster_embeddings(embeddings, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(embeddings)
    return clusters

def get_cluster_centers(embeddings, clusters):
    unique_clusters = np.unique(clusters)
    centers = []
    for cluster in unique_clusters:
        cluster_points = embeddings[clusters == cluster]
        center = np.mean(cluster_points, axis=0)
        centers.append(center)
    return np.array(centers)