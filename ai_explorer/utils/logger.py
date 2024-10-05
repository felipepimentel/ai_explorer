import logging
from config import Config

logging.basicConfig(level=Config.LOGGING_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_logger(name):
    return logging.getLogger(name)
