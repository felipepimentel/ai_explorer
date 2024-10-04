from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

class RealtimeTopicDetector:
    def __init__(self, num_topics=5, window_size=100):
        self.num_topics = num_topics
        self.window_size = window_size
        self.vectorizer = CountVectorizer(stop_words='english')
        self.document_buffer = []

    def add_document(self, document):
        self.document_buffer.append(document)
        if len(self.document_buffer) > self.window_size:
            self.document_buffer.pop(0)

    def detect_topics(self):
        if not self.document_buffer:
            return []

        X = self.vectorizer.fit_transform(self.document_buffer)
        feature_names = np.array(self.vectorizer.get_feature_names())
        
        word_counts = X.sum(axis=0).A1
        top_word_indices = word_counts.argsort()[-self.num_topics:][::-1]
        
        return [
            {"word": feature_names[i], "count": word_counts[i]}
            for i in top_word_indices
        ]

# Uso:
# detector = RealtimeTopicDetector()
# detector.add_document("New AI breakthrough in natural language processing")
# detector.add_document("Stock market reaches all-time high")
# topics = detector.detect_topics()