import spacy
from spacy.matcher import Matcher

class InconsistencyDetector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        
        # Define padrões para detectar inconsistências
        self.matcher.add("INCONSISTENCY", [
            [{"LOWER": "however"}, {"OP": "*"}, {"LOWER": "not"}],
            [{"LOWER": "although"}, {"OP": "*"}, {"LOWER": "contrary"}],
            # Adicione mais padrões conforme necessário
        ])

    def detect_inconsistencies(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        inconsistencies = []
        for match_id, start, end in matches:
            span = doc[start:end]
            inconsistencies.append({
                "text": span.text,
                "start": start,
                "end": end
            })
        
        return inconsistencies

# Uso:
# detector = InconsistencyDetector()
# inconsistencies = detector.detect_inconsistencies("The product is great. However, it's not worth the price.")