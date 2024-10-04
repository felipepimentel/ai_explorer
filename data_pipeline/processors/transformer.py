from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Transformer:
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def transform(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.logits.squeeze().numpy()

def apply_transformation(text, model_name='bert-base-uncased'):
    transformer = Transformer(model_name)
    return transformer.transform(text)