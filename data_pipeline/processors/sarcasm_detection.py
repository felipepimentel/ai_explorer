from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SarcasmDetector:
    def __init__(self, model_name="deepset/roberta-base-squad2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    def detect_sarcasm(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sarcasm_probability = probabilities[0][1].item()
        
        return {
            "text": text,
            "sarcasm_probability": sarcasm_probability,
            "is_sarcastic": sarcasm_probability > 0.5
        }

# Uso:
# detector = SarcasmDetector()
# result = detector.detect_sarcasm("Oh great, another meeting. Just what I needed to make my day complete.")