import time
from functools import wraps
from config import Config
from utils.logger import get_logger

logger = get_logger("performance_monitor")

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not Config.PERFORMANCE_MONITORING_ENABLED:
            return func(*args, **kwargs)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {elapsed_time:.2f} seconds with args: {args}, kwargs: {kwargs}")
        return result
    return wrapper
