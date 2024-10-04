from transformers import pipeline

class TextCorrector:
    def __init__(self, model_name="vennify/t5-base-grammar-correction"):
        self.corrector = pipeline("text2text-generation", model=model_name)

    def correct_text(self, text):
        corrected = self.corrector(f"grammar: {text}", max_length=len(text) + 50)
        return corrected[0]['generated_text']

# Uso:
# corrector = TextCorrector()
# corrected_text = corrector.correct_text("This is an example of an text with mistakes.")