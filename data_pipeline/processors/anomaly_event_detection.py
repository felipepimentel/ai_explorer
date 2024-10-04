import numpy as np
from sklearn.ensemble import IsolationForest
from data_pipeline.processors.embedding import EmbeddingModel

class AnomalyEventDetector:
    def __init__(self, contamination=0.1):
        self.embedder = EmbeddingModel()
        self.detector = IsolationForest(contamination=contamination)

    def detect_anomalies(self, documents, timestamps):
        embeddings = np.array([self.embedder.generate_text_embeddings(doc) for doc in documents])
        self.detector.fit(embeddings)
        
        anomaly_scores = self.detector.decision_function(embeddings)
        anomalies = self.detector.predict(embeddings)
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'document': documents,
            'anomaly_score': anomaly_scores,
            'is_anomaly': anomalies == -1
        }).sort_values('anomaly_score')

# Uso:
# detector = AnomalyEventDetector()
# anomalies = detector.detect_anomalies(documents, timestamps)