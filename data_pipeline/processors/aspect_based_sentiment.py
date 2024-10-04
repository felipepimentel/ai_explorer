from transformers import pipeline

class AspectBasedSentimentAnalyzer:
    def __init__(self):
        self.nlp = pipeline("sentiment-analysis")

    def analyze_aspect_sentiment(self, text, aspects):
        results = []
        for aspect in aspects:
            sentiment = self.nlp(f"{aspect}: {text}")[0]
            results.append({
                "aspect": aspect,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })
        return results

# Uso:
# analyzer = AspectBasedSentimentAnalyzer()
# aspects = ["price", "quality", "service"]
# results = analyzer.analyze_aspect_sentiment("The food was great but a bit expensive. The service was excellent.", aspects)