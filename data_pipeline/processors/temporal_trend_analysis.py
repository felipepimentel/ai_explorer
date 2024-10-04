from data_pipeline.processors.base_processor import BaseProcessor
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class TemporalTrendAnalyzer(BaseProcessor):
    def __init__(self, time_window='D'):
        self.time_window = time_window
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def process(self, input_data):
        documents, timestamps = input_data
        return self.analyze_trends(documents, timestamps)

    def batch_process(self, input_data_list):
        return [self.process(input_data) for input_data in input_data_list]

    def analyze_trends(self, documents, timestamps):
        df = pd.DataFrame({'document': documents, 'timestamp': pd.to_datetime(timestamps)})
        df = df.set_index('timestamp').sort_index()
        
        trends = df.groupby(pd.Grouper(freq=self.time_window)).apply(self._analyze_period)
        return trends

    def _analyze_period(self, group):
        if group.empty:
            return pd.Series()
        
        tfidf = self.vectorizer.fit_transform(group['document'])
        feature_names = np.array(self.vectorizer.get_feature_names())
        
        tfidf_sum = tfidf.sum(axis=0).A1
        top_indices = tfidf_sum.argsort()[-10:][::-1]
        
        return pd.Series({
            'top_terms': list(zip(feature_names[top_indices], tfidf_sum[top_indices])),
            'document_count': len(group)
        })

    def plot_trend(self, trend_data, term):
        term_trend = trend_data.apply(lambda x: dict(x['top_terms']).get(term, 0) if isinstance(x['top_terms'], list) else 0)
        return term_trend.plot(title=f"Trend for '{term}'")

# Uso:
# analyzer = TemporalTrendAnalyzer()
# trends = analyzer.analyze_trends(documents, timestamps)
# analyzer.plot_trend(trends, 'ai')