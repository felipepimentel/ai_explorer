from gensim import corpora
from gensim.models import LdaMulticore
import pandas as pd
import numpy as np

class TopicEvolutionAnalyzer:
    def __init__(self, num_topics=10):
        self.num_topics = num_topics
        self.dictionary = None
        self.lda_model = None

    def preprocess(self, texts):
        return [[word for word in document.lower().split() if word.isalnum()] for document in texts]

    def fit(self, documents, timestamps):
        preprocessed_docs = self.preprocess(documents)
        self.dictionary = corpora.Dictionary(preprocessed_docs)
        corpus = [self.dictionary.doc2bow(doc) for doc in preprocessed_docs]
        self.lda_model = LdaMulticore(corpus=corpus, id2word=self.dictionary, num_topics=self.num_topics)
        
        df = pd.DataFrame({'document': documents, 'timestamp': pd.to_datetime(timestamps)})
        df['topics'] = df['document'].apply(lambda x: self.lda_model.get_document_topics(self.dictionary.doc2bow(x.lower().split())))
        
        return df

    def analyze_evolution(self, df, time_window='M'):
        topic_evolution = df.set_index('timestamp').groupby(pd.Grouper(freq=time_window)).agg({
            'topics': lambda x: np.mean([dict(t) for t in x], axis=0)
        })
        
        return topic_evolution

# Uso:
# analyzer = TopicEvolutionAnalyzer()
# df = analyzer.fit(documents, timestamps)
# evolution = analyzer.analyze_evolution(df)