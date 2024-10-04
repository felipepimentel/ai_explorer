import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CoherenceAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_coherence(self, text):
        doc = self.nlp(text)
        sentences = list(doc.sents)
        
        if len(sentences) < 2:
            return 1.0  # Perfeitamente coerente se houver apenas uma sentença
        
        sentence_embeddings = [sent.vector for sent in sentences]
        similarities = cosine_similarity(sentence_embeddings)
        
        # Calcular a média das similaridades entre sentenças adjacentes
        coherence_score = np.mean([similarities[i][i+1] for i in range(len(sentences)-1)])
        
        return coherence_score

# Uso:
# analyzer = CoherenceAnalyzer()
# coherence = analyzer.analyze_coherence("This is a coherent text. It has related sentences. The topic is consistent.")