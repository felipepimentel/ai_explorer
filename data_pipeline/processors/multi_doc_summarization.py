from transformers import pipeline
from data_pipeline.processors.text_summarization import TextSummarizer

class MultiDocSummarizer:
    def __init__(self):
        self.summarizer = TextSummarizer()

    def summarize_multiple_documents(self, documents, max_length=150):
        individual_summaries = [self.summarizer.summarize(doc, max_length=max_length) for doc in documents]
        combined_summary = " ".join(individual_summaries)
        final_summary = self.summarizer.summarize(combined_summary, max_length=max_length)
        return final_summary

# Uso:
# summarizer = MultiDocSummarizer()
# summary = summarizer.summarize_multiple_documents(["Doc1 content", "Doc2 content", "Doc3 content"])