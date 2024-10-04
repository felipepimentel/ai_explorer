import spacy
from collections import Counter

class WritingStyleAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_style(self, text):
        doc = self.nlp(text)
        
        # Análise de complexidade sintática
        sentence_lengths = [len([token for token in sent if not token.is_punct]) for sent in doc.sents]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
        
        # Análise de diversidade lexical
        lexical_diversity = len(set([token.lemma_ for token in doc if not token.is_punct])) / len([token for token in doc if not token.is_punct])
        
        # Análise de uso de voz passiva
        passive_constructions = len([token for token in doc if token.dep_ == "nsubjpass"])
        
        # Análise de uso de adjetivos e advérbios
        pos_counts = Counter([token.pos_ for token in doc])
        
        return {
            "avg_sentence_length": avg_sentence_length,
            "lexical_diversity": lexical_diversity,
            "passive_constructions": passive_constructions,
            "adjective_ratio": pos_counts["ADJ"] / len(doc),
            "adverb_ratio": pos_counts["ADV"] / len(doc)
        }

# Uso:
# analyzer = WritingStyleAnalyzer()
# style_metrics = analyzer.analyze_style("This is a sample text to analyze for writing style.")