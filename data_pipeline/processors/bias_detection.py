import spacy
from collections import Counter

class BiasDetector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.gender_words = {
            "male": ["he", "him", "his", "man", "men", "boy", "boys"],
            "female": ["she", "her", "hers", "woman", "women", "girl", "girls"]
        }

    def detect_gender_bias(self, text):
        doc = self.nlp(text.lower())
        gender_counts = {"male": 0, "female": 0}
        
        for token in doc:
            if token.text in self.gender_words["male"]:
                gender_counts["male"] += 1
            elif token.text in self.gender_words["female"]:
                gender_counts["female"] += 1
        
        total = sum(gender_counts.values())
        if total == 0:
            return 0  # No gender bias detected
        
        bias_score = abs(gender_counts["male"] - gender_counts["female"]) / total
        return bias_score

# Uso:
# detector = BiasDetector()
# bias_score = detector.detect_gender_bias("He went to the store. She cooked dinner.")