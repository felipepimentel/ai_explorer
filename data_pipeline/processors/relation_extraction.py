import spacy
from spacy.tokens import Span

class RelationExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_relations(self, text):
        doc = self.nlp(text)
        relations = []
        
        for entity in doc.ents:
            if entity.label_ == "PERSON":
                for possible_relation in doc[entity.end:]:
                    if possible_relation.dep_ == "ROOT" and possible_relation.pos_ == "VERB":
                        for obj in possible_relation.children:
                            if obj.dep_ == "dobj" and obj.ent_type_:
                                relations.append((entity.text, possible_relation.text, obj.text))
                                break
                        break
        
        return relations

# Uso:
# extractor = RelationExtractor()
# relations = extractor.extract_relations("John visited Paris last summer.")