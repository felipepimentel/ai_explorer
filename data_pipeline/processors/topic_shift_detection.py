from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TopicShiftDetector:
    def __init__(self, window_size=100, threshold=0.7):
        self.window_size = window_size
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.document_buffer = []
        self.previous_centroid = None

    def add_document(self, document):
        self.document_buffer.append(document)
        if len(self.document_buffer) > self.window_size:
            self.document_buffer.pop(0)

        return self.detect_shift()

    def detect_shift(self):
        if len(self.document_buffer) < self.window_size:
            return False

        tfidf = self.vectorizer.fit_transform(self.document_buffer)
        centroid = tfidf.mean(axis=0)

        if self.previous_centroid is not None:
            similarity = cosine_similarity(self.previous_centroid, centroid)[0][0]
            if similarity < self.threshold:
                self.previous_centroid = centroid
                return True

        self.previous_centroid = centroid
        return False

# Uso:
# detector = TopicShiftDetector()
# for document in stream_of_documents:
#     if detector.add_document(document):
#         print("Topic shift detected!")