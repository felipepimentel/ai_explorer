from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # Para resultados consistentes

class LanguageDetector:
    def __init__(self):
        pass

    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return "unknown"

    def detect_languages_batch(self, texts):
        return [self.detect_language(text) for text in texts]

# Uso:
# detector = LanguageDetector()
# language = detector.detect_language("This is an English text.")
# languages = detector.detect_languages_batch(["This is English", "Esto es español", "Das ist Deutsch"])