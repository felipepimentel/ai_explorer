from PIL import Image
import pytesseract
import numpy as np
from transformers import ViTFeatureExtractor, ViTModel

class ImageProcessor:
    def __init__(self, model_name='google/vit-base-patch16-224'):
        self.feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
        self.model = ViTModel.from_pretrained(model_name)

    def extract_text(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def generate_embedding(self, image_path):
        image = Image.open(image_path)
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0].detach().numpy()

def process_image(image_path):
    processor = ImageProcessor()
    text = processor.extract_text(image_path)
    embedding = processor.generate_embedding(image_path)
    return {"text": text, "embedding": embedding}