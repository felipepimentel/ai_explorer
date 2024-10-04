import numpy as np
from ruptures import Pelt
import pandas as pd

class ChangePointDetector:
    def __init__(self, penalty=10):
        self.algo = Pelt(model="rbf").fit(penalty=penalty)

    def detect_change_points(self, time_series):
        change_points = self.algo.predict(time_series)
        return change_points[:-1]  # Exclude the last point which is always the series length

    def analyze_time_series(self, dates, values):
        df = pd.DataFrame({'date': pd.to_datetime(dates), 'value': values})
        df = df.sort_values('date')
        
        change_points = self.detect_change_points(df['value'].values)
        
        result = []
        for cp in change_points:
            result.append({
                'date': df.iloc[cp]['date'],
                'value': df.iloc[cp]['value']
            })
        
        return result

# Uso:
# detector = ChangePointDetector()
# change_points = detector.analyze_time_series(dates, values)