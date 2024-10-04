import spacy
import textstat

class TextComplexityAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_complexity(self, text):
        doc = self.nlp(text)
        
        return {
            "sentence_count": len(list(doc.sents)),
            "word_count": len([token for token in doc if not token.is_punct]),
            "avg_sentence_length": sum(len([token for token in sent if not token.is_punct]) for sent in doc.sents) / len(list(doc.sents)),
            "avg_word_length": sum(len(token.text) for token in doc if not token.is_punct) / len([token for token in doc if not token.is_punct]),
            "flesch_reading_ease": textstat.flesch_reading_ease(text),
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
            "difficult_words_ratio": textstat.difficult_words(text) / len([token for token in doc if not token.is_punct])
        }

# Uso:
# analyzer = TextComplexityAnalyzer()
# complexity_scores = analyzer.analyze_complexity("This is a sample text to analyze for complexity.")