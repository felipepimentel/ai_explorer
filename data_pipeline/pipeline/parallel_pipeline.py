from concurrent.futures import ProcessPoolExecutor
from data_pipeline.pipeline.pipeline import Pipeline

class ParallelPipeline(Pipeline):
    def __init__(self, max_workers=None):
        super().__init__()
        self.max_workers = max_workers

    def batch_process(self, input_data_list):
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            for step in self.steps:
                input_data_list = list(executor.map(step.process, input_data_list))
        return input_data_list

# Uso:
# pipeline = ParallelPipeline(max_workers=4)
# pipeline.add_step(TemporalTrendAnalyzer())
# pipeline.add_step(AnomalyEventDetector())
# results = pipeline.batch_process(input_data_list)