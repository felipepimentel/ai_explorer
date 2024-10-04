from transformers import pipeline

class AspectFocusedSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text, aspect, max_length=150, min_length=50):
        prompt = f"Summarize the following text focusing on {aspect}:\n\n{text}"
        summary = self.summarizer(prompt, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

# Uso:
# summarizer = AspectFocusedSummarizer()
# summary = summarizer.summarize("Long text about a product...", aspect="price and quality")