import PyPDF2
import pytesseract
from PIL import Image
import whisper
from transformers import T5Tokenizer, T5Model
from functools import lru_cache

class EmbeddingModel:
    def __init__(self, tokenizer_model="t5-base", whisper_model="base"):
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_model)
        self.t5_model = T5Model.from_pretrained(tokenizer_model)
        self.whisper_model = whisper.load_model(whisper_model)

    @lru_cache(maxsize=100)
    def generate_text_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.t5_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()

    def generate_pdf_embeddings(self, filepath):
        content = self._extract_pdf_text(filepath)
        return self.generate_text_embeddings(content)

    def generate_image_embeddings(self, filepath):
        content = self._extract_image_text(filepath)
        return self.generate_text_embeddings(content)

    def generate_audio_embeddings(self, filepath):
        content = self._transcribe_audio(filepath)
        return self.generate_text_embeddings(content)

    def _extract_pdf_text(self, filepath):
        pdf_reader = PyPDF2.PdfReader(filepath)
        return ''.join([page.extract_text() for page in pdf_reader.pages])

    def _extract_image_text(self, filepath):
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)

    def _transcribe_audio(self, filepath):
        transcription = self.whisper_model.transcribe(filepath)
        return transcription['text']

def get_embedder(model_name='t5-base'):
    return EmbeddingModel(tokenizer_model=model_name)