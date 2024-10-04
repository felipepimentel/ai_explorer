import spacy
import pandas as pd
from collections import defaultdict

class EntityEvolutionAnalyzer:
    def __init__(self, time_window='D'):
        self.nlp = spacy.load("en_core_web_sm")
        self.time_window = time_window

    def analyze_evolution(self, documents, timestamps):
        df = pd.DataFrame({'document': documents, 'timestamp': pd.to_datetime(timestamps)})
        df = df.set_index('timestamp').sort_index()
        
        evolution = df.groupby(pd.Grouper(freq=self.time_window)).apply(self._analyze_period)
        return evolution

    def _analyze_period(self, group):
        entities = defaultdict(lambda: defaultdict(int))
        for doc in self.nlp.pipe(group['document']):
            for ent in doc.ents:
                entities[ent.label_][ent.text] += 1
        
        return pd.Series({
            'entities': dict(entities),
            'document_count': len(group)
        })

    def plot_entity_evolution(self, evolution_data, entity_type, top_n=5):
        entity_counts = evolution_data['entities'].apply(lambda x: x.get(entity_type, {}))
        top_entities = Counter([item for sublist in entity_counts for item in sublist]).most_common(top_n)
        
        df = pd.DataFrame({entity: entity_counts.apply(lambda x: x.get(entity, 0)) for entity, _ in top_entities})
        return df.plot(title=f"Evolution of top {top_n} {entity_type} entities")

# Uso:
# analyzer = EntityEvolutionAnalyzer()
# evolution = analyzer.analyze_evolution(documents, timestamps)
# analyzer.plot_entity_evolution(evolution, 'PERSON')