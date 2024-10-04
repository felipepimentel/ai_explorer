import spacy
from collections import defaultdict

class BiasDetectorCorrector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.bias_words = {
            "gender": {
                "biased": {"he": "they", "she": "they", "man": "person", "woman": "person"},
                "neutral": {"they", "person", "individual"}
            },
            "race": {
                "biased": {"black": "person of color", "white": "person"},
                "neutral": {"person of color", "individual"}
            }
            # Add more categories and words as needed
        }

    def detect_bias(self, text):
        doc = self.nlp(text)
        biases = defaultdict(list)
        
        for token in doc:
            for category, words in self.bias_words.items():
                if token.text.lower() in words["biased"]:
                    biases[category].append(token.text)
        
        return dict(biases)

    def correct_bias(self, text):
        doc = self.nlp(text)
        corrected_tokens = []
        
        for token in doc:
            corrected = token.text
            for category, words in self.bias_words.items():
                if token.text.lower() in words["biased"]:
                    corrected = words["biased"].get(token.text.lower(), token.text)
            corrected_tokens.append(corrected)
        
        return " ".join(corrected_tokens)

# Uso:
# detector_corrector = BiasDetectorCorrector()
# biases = detector_corrector.detect_bias("The chairman called her into his office.")
# corrected_text = detector_corrector.correct_bias("The chairman called her into his office.")