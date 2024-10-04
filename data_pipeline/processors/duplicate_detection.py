from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DuplicateDetector:
    def __init__(self, threshold=0.9):
        self.vectorizer = TfidfVectorizer()
        self.threshold = threshold

    def find_duplicates(self, documents):
        vectors = self.vectorizer.fit_transform(documents)
        similarity_matrix = cosine_similarity(vectors)
        np.fill_diagonal(similarity_matrix, 0)
        
        duplicates = []
        for i in range(len(documents)):
            for j in range(i+1, len(documents)):
                if similarity_matrix[i][j] > self.threshold:
                    duplicates.append((i, j, similarity_matrix[i][j]))
        
        return duplicates

# Uso:
# detector = DuplicateDetector()
# duplicates = detector.find_duplicates(["Doc1", "Doc2", "Doc3", "Almost identical to Doc1"])