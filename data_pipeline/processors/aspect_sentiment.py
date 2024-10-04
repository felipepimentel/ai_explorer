from transformers import pipeline
import spacy

class AspectSentimentAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def analyze_aspect_sentiment(self, text):
        doc = self.nlp(text)
        aspects = [chunk.text for chunk in doc.noun_chunks]
        
        results = []
        for aspect in aspects:
            sentiment = self.sentiment_analyzer(f"{aspect}: {text}")[0]
            results.append({
                "aspect": aspect,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })
        
        return results

# Uso:
# analyzer = AspectSentimentAnalyzer()
# results = analyzer.analyze_aspect_sentiment("The food was great but the service was terrible.")