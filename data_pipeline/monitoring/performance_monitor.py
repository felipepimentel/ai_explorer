import time
from functools import wraps
from data_pipeline.utils.logger import setup_logger

logger = setup_logger(__name__, 'logs/performance.log')

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper

# Uso:
# @monitor_performance
# def some_function():
#     # function code here