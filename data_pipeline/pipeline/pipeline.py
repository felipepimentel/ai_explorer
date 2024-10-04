class Pipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, processor):
        self.steps.append(processor)
        return self

    def process(self, input_data):
        for step in self.steps:
            input_data = step.process(input_data)
        return input_data

    def batch_process(self, input_data_list):
        for step in self.steps:
            input_data_list = step.batch_process(input_data_list)
        return input_data_list

# Uso:
# from data_pipeline.processors.temporal_trend_analysis import TemporalTrendAnalyzer
# from data_pipeline.processors.anomaly_event_detection import AnomalyEventDetector
# 
# pipeline = Pipeline()
# pipeline.add_step(TemporalTrendAnalyzer())
# pipeline.add_step(AnomalyEventDetector())
# 
# result = pipeline.process((documents, timestamps))