import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Configurar o logger principal
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)
main_logger = setup_logger('main_logger', os.path.join(log_directory, 'main.log'))