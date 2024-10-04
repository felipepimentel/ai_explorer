from rake_nltk import Rake
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class KeywordExtractor:
    def __init__(self):
        self.rake = Rake()

    def extract_keywords(self, text, top_n=5):
        self.rake.extract_keywords_from_text(text)
        return self.rake.get_ranked_phrases()[:top_n]

# Uso:
# extractor = KeywordExtractor()
# keywords = extractor.extract_keywords("Text to extract keywords from")