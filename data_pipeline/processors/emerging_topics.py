import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class EmergingTopicDetector:
    def __init__(self, n_topics=5):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)

    def detect_topics(self, documents, time_windows):
        X = self.vectorizer.fit_transform(documents)
        feature_names = self.vectorizer.get_feature_names()
        
        topic_evolution = []
        for window in time_windows:
            window_docs = X[window]
            self.lda.fit(window_docs)
            topics = self._get_top_words(self.lda, feature_names)
            topic_evolution.append(topics)
        
        return topic_evolution

    def _get_top_words(self, model, feature_names, n_top_words=10):
        topics = []
        for topic_idx, topic in enumerate(model.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            topics.append(top_words)
        return topics

# Uso:
# detector = EmergingTopicDetector()
# topic_evolution = detector.detect_topics(documents, time_windows)