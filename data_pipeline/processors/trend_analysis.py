from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from data_pipeline.processors.keyword_extraction import KeywordExtractor

class TrendAnalyzer:
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()

    def analyze_trends(self, documents, timestamps):
        df = pd.DataFrame({'document': documents, 'timestamp': timestamps})
        df['keywords'] = df['document'].apply(self.keyword_extractor.extract_keywords)
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        
        trend_data = {}
        for date, group in df.groupby('date'):
            keywords = [kw for kws in group['keywords'] for kw in kws]
            trend_data[date] = Counter(keywords)
        
        return pd.DataFrame(trend_data).fillna(0)

    def plot_trends(self, trend_data, top_n=5):
        top_keywords = trend_data.sum().nlargest(top_n).index
        plt.figure(figsize=(12, 6))
        for keyword in top_keywords:
            plt.plot(trend_data.index, trend_data[keyword], label=keyword)
        plt.legend()
        plt.title(f"Top {top_n} Keyword Trends")
        plt.xlabel("Date")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt

# Uso:
# analyzer = TrendAnalyzer()
# trends = analyzer.analyze_trends(documents, timestamps)
# plot = analyzer.plot_trends(trends)
# plot.show()