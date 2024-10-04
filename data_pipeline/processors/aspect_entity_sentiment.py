import spacy
from transformers import pipeline

class AspectEntitySentimentAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def analyze(self, text):
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        aspects = [chunk.text for chunk in doc.noun_chunks]
        
        results = []
        for aspect in set(aspects + [ent[0] for ent in entities]):
            sentiment = self.sentiment_analyzer(f"{aspect}: {text}")[0]
            results.append({
                "aspect": aspect,
                "entity_type": next((ent[1] for ent in entities if ent[0] == aspect), None),
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })
        
        return results

# Uso:
# analyzer = AspectEntitySentimentAnalyzer()
# results = analyzer.analyze("Apple's new iPhone has an excellent camera, but the battery life is disappointing.")