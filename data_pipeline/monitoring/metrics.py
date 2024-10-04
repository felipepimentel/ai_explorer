import time
from functools import wraps
from prometheus_client import Counter, Histogram, start_http_server

# Métricas
PROCESSED_FILES = Counter('processed_files_total', 'Number of files processed')
PROCESSING_TIME = Histogram('file_processing_seconds', 'Time spent processing files')

def track_metrics(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        PROCESSED_FILES.inc()
        PROCESSING_TIME.observe(time.time() - start_time)
        return result
    return wrapper

def start_metrics_server(port=8000):
    start_http_server(port)

# Uso:
# from data_pipeline.monitoring.metrics import track_metrics, start_metrics_server
# @track_metrics
# def process_file(file_path):
#     # Processamento do arquivo...
#
# if __name__ == "__main__":
#     start_metrics_server()