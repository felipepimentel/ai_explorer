import importlib

class DependencyManager:
    @staticmethod
    def load_processor(processor_name):
        try:
            module = importlib.import_module(f"data_pipeline.processors.{processor_name}")
            return getattr(module, processor_name.capitalize())
        except (ImportError, AttributeError):
            raise ValueError(f"Processor {processor_name} not found")

# Uso:
# processor_class = DependencyManager.load_processor("temporal_trend_analysis")
# processor = processor_class()