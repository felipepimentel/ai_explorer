import functools
import os
import time

import psutil

from .app import logger, notification_service
from .config import Config


def log_message(level: str, message: str) -> None:
    getattr(logger, level)(message)


def monitor_performance(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        log_message(
            "info",
            f"{func.__name__} - Time: {execution_time:.2f}s, CPU: {cpu_usage}%, Memory: {memory_usage}%",
        )
        return result

    return wrapper


def load_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def ensure_directory_exists(directory_path: str) -> None:
    os.makedirs(directory_path, exist_ok=True)


def handle_exception(e: Exception, message: str = "An error occurred") -> None:
    log_message("error", f"{message}: {str(e)}")
    notification_service.notify(f"{message}. Check logs for details.")


def check_system_resources() -> None:
    if psutil.cpu_percent() > Config.CPU_LIMIT * 100:
        log_message("warning", "CPU usage is above limit, throttling operations.")
        time.sleep(1)
    if psutil.virtual_memory().percent > Config.MEMORY_LIMIT * 100:
        log_message("warning", "Memory usage is above limit, throttling operations.")
        time.sleep(1)


def clean_temp_files() -> None:
    now = time.time()
    for filename in os.listdir(Config.TEMP_DIR):
        file_path = os.path.join(Config.TEMP_DIR, filename)
        if os.stat(file_path).st_mtime < now - Config.TEMP_FILE_RETENTION:
            os.remove(file_path)
