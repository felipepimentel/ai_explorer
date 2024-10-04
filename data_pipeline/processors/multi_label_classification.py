from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.preprocessing import MultiLabelBinarizer

class MultiLabelClassifier:
    def __init__(self, model_name='bert-base-uncased', num_labels=10):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.mlb = MultiLabelBinarizer()

    def train(self, texts, labels):
        self.mlb.fit(labels)
        encoded_labels = self.mlb.transform(labels)
        
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs, labels=torch.tensor(encoded_labels).float())
        loss = outputs.loss
        loss.backward()
        # Implement optimizer step and training loop

    def predict(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        predictions = torch.sigmoid(outputs.logits).detach().numpy()
        return self.mlb.inverse_transform(predictions > 0.5)

# Uso:
# classifier = MultiLabelClassifier(num_labels=5)
# classifier.train(["text1", "text2"], [["label1", "label2"], ["label2", "label3"]])
# predictions = classifier.predict(["new text"])