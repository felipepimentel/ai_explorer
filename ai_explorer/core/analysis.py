import difflib
import os
import time
from typing import List, Tuple

import faiss
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from cachetools import TTLCache, cached
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

from ..app import nlp
from ..config import Config
from ..infrastructure.database import database_service
from ..utils import load_file, log_message
from .embedding import EmbeddingService
from .models import FileType


class AnalysisService:
    def __init__(self):
        self.index = faiss.IndexFlatIP(Config.EMBEDDING_DIM)
        self.file_paths: List[str] = []
        self.timestamps: List[float] = []
        self.topic_model = None
        self.vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.kmeans = KMeans(n_clusters=Config.NUM_CLUSTERS)
        self.cluster_labels: List[int] = []

    def add_embeddings_to_index(
        self, embeddings: List[np.array], file_paths: List[str]
    ) -> None:
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.file_paths.extend(file_paths)
        self.timestamps.extend([time.time()] * len(file_paths))
        self.update_clusters(embeddings)
        self.update_data_lineage(file_paths)

    def update_clusters(self, new_embeddings: np.array) -> None:
        all_embeddings = np.array(self.index.reconstruct_n(0, self.index.ntotal))
        self.cluster_labels = self.kmeans.fit_predict(all_embeddings)

    def search_embeddings(
        self, query_embedding: np.array, k: int = 5
    ) -> List[Tuple[str, float]]:
        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, k)
        results = [
            (self.file_paths[idx], float(distances[0][i]))
            for i, idx in enumerate(indices[0])
        ]
        return results

    @cached(cache=TTLCache(maxsize=100, ttl=Config.SEARCH_CACHE_TTL))
    def search(
        self,
        query: str,
        embedding_service: EmbeddingService,
        data_type: FileType = FileType.TEXT,
        k: int = 5,
    ) -> List[Tuple[str, float]]:
        query_embedding = embedding_service.embed(query, data_type)
        query_embedding /= np.linalg.norm(query_embedding)
        results = self.search_embeddings(query_embedding, k)
        return results

    def incremental_indexing(
        self, embeddings: List[np.array], file_paths: List[str]
    ) -> None:
        self.add_embeddings_to_index(embeddings, file_paths)

    def topic_analysis(self, documents: List[str], num_topics: int = 5) -> np.array:
        dtm = self.vectorizer.fit_transform(documents)
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(dtm)
        topics = lda.transform(dtm)
        return topics

    def version_control(self, file_path: str, content_hash: str) -> bool:
        existing_hash = database_service.get_file_hash(file_path)
        if existing_hash != content_hash:
            version = len(database_service.get_file_versions(file_path)) + 1
            database_service.add_file_version(file_path, version, content_hash)
            database_service.update_file_hash(file_path, content_hash)
            return True
        return False

    def visualize_similarity_graph(self):
        G = self._create_similarity_graph()
        self._draw_graph(G)

    def _create_similarity_graph(self):
        G = nx.Graph()
        embeddings = np.zeros((self.index.ntotal, self.index.d))
        self.index.reconstruct_n(0, self.index.ntotal, embeddings)
        similarity_matrix = cosine_similarity(embeddings)
        for i in range(len(self.file_paths)):
            for j in range(i + 1, len(self.file_paths)):
                if similarity_matrix[i, j] > Config.SIMILARITY_THRESHOLD:
                    G.add_edge(
                        self.file_paths[i],
                        self.file_paths[j],
                        weight=similarity_matrix[i, j],
                    )
        return G

    def _draw_graph(self, G):
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=8,
            font_weight="bold",
        )
        plt.title("Document Similarity Graph")
        plt.tight_layout()
        plt.show()

    def analyze_sentiment(self, texts):
        sentiments = [
            self.sentiment_analyzer.polarity_scores(text)["compound"] for text in texts
        ]
        return sentiments

    def sentiment_analysis_multimodal(self, texts, audios):
        text_sentiments = self.analyze_sentiment(texts)
        audio_sentiments = [
            0.0 for _ in audios
        ]  # Placeholder for audio sentiment analysis
        combined_sentiments = [
            (t + a) / 2 for t, a in zip(text_sentiments, audio_sentiments)
        ]
        return combined_sentiments

    def question_answering(self, question, context):
        qa_pipeline = pipeline("question-answering")
        result = qa_pipeline(question=question, context=context)
        return result["answer"]

    def generate_insights(self, file_path):
        text = load_file(file_path)
        topics = self.topic_analysis([text])
        sentiment = self.sentiment_analysis_multimodal([text], [])
        return {
            "topics": topics.tolist(),
            "sentiment": sentiment[0],
            "file_path": file_path,
        }

    def get_cluster_info(self):
        cluster_info = {}
        for i, label in enumerate(self.cluster_labels):
            if label not in cluster_info:
                cluster_info[label] = []
            cluster_info[label].append(self.file_paths[i])
        return cluster_info

    def update_data_lineage(self, file_paths):
        for file_path in file_paths:
            database_service.update_data_lineage(file_path)

    def deduplicate_embeddings(self):
        embeddings = np.zeros((self.index.ntotal, self.index.d))
        self.index.reconstruct_n(0, self.index.ntotal, embeddings)
        unique_embeddings, unique_indices = np.unique(
            embeddings, axis=0, return_index=True
        )
        self.index = faiss.IndexFlatIP(Config.EMBEDDING_DIM)
        self.index.add(unique_embeddings)
        self.file_paths = [self.file_paths[i] for i in unique_indices]
        self.timestamps = [self.timestamps[i] for i in unique_indices]

    def enrich_data(self, file_path, text):
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        categories = self.topic_analysis([text], num_topics=1)[0].tolist()
        tags = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
        enriched_data = {"entities": entities, "categories": categories, "tags": tags}
        print(f"Enriched data for {file_path}: {enriched_data}")

    def partition_data(self, file_path):
        metadata = database_service.get_file_metadata(file_path)
        partition_key = metadata.creation_date.strftime("%Y-%m-%d")
        return partition_key

    def apply_retention_policy(self):
        current_time = time.time()
        files_to_remove = []
        for i, (file_path, timestamp) in enumerate(
            zip(self.file_paths, self.timestamps)
        ):
            if current_time - timestamp > Config.RETENTION_PERIOD:
                files_to_remove.append((i, file_path))

        for index, file_path in reversed(files_to_remove):
            del self.file_paths[index]
            del self.timestamps[index]
            self.index.remove_ids(np.array([index]))
            print(f"Removed {file_path} due to retention policy")

    def monitor_storage_size(self):
        total_size = sum(
            os.path.getsize(f) for f in self.file_paths if os.path.isfile(f)
        )
        if total_size > Config.MAX_STORAGE_SIZE:
            log_message("warning", f"Storage size exceeded: {total_size} bytes")
            self.apply_retention_policy()

    def temporal_analysis(self, start_date, end_date):
        print(f"Temporal analysis from {start_date} to {end_date}")
        return []

    def compare_versions(self, file_path, version1, version2):
        versions = database_service.get_file_versions(file_path)
        content1 = self.get_version_content(file_path, version1)
        content2 = self.get_version_content(file_path, version2)

        differ = difflib.Differ()
        diff = list(differ.compare(content1.splitlines(), content2.splitlines()))
        return "\n".join(diff)

    def get_version_content(self, file_path, version):
        return f"Content of {file_path} version {version}"
