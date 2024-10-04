from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        self.sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

    def analyze(self, text):
        result = self.sentiment_pipeline(text)[0]
        return {
            "label": result["label"],
            "score": result["score"]
        }

    def analyze_batch(self, texts):
        results = self.sentiment_pipeline(texts)
        return [{"label": result["label"], "score": result["score"]} for result in results]

# Uso:
# analyzer = SentimentAnalyzer()
# sentiment = analyzer.analyze("I love this product!")
# batch_sentiments = analyzer.analyze_batch(["I love this", "I hate this"])