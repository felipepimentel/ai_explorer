from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class NERProcessor:
    def __init__(self, model_name="dbmdz/bert-large-cased-finetuned-conll03-english"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")

    def extract_entities(self, text):
        return self.ner_pipeline(text)

    def enrich_document(self, document):
        entities = self.extract_entities(document)
        enriched_doc = {
            "text": document,
            "entities": entities
        }
        return enriched_doc

# Uso:
# ner_processor = NERProcessor()
# enriched_doc = ner_processor.enrich_document("Apple Inc. was founded by Steve Jobs in Cupertino, California.")