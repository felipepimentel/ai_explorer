import numpy as np
from sklearn.ensemble import IsolationForest
from data_pipeline.processors.contextual_embeddings import ContextualEmbedder

class TextAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.embedder = ContextualEmbedder()
        self.model = IsolationForest(contamination=contamination)

    def fit(self, texts):
        embeddings = self.embedder.generate_batch_embeddings(texts)
        self.model.fit(embeddings)

    def detect_anomalies(self, texts):
        embeddings = self.embedder.generate_batch_embeddings(texts)
        predictions = self.model.predict(embeddings)
        return [text for text, pred in zip(texts, predictions) if pred == -1]

# Uso:
# detector = TextAnomalyDetector()
# detector.fit(["Normal text 1", "Normal text 2", ...])
# anomalies = detector.detect_anomalies(["Test text 1", "Test text 2", ...])