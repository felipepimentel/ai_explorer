import logging
import traceback
from data_pipeline.utils.logger import setup_logger

logger = setup_logger(__name__, 'logs/errors.log')

class DataPipelineError(Exception):
    """Base exception class for Data Pipeline errors."""
    pass

class FileProcessingError(DataPipelineError):
    """Raised when there's an error processing a file."""
    pass

class EmbeddingError(DataPipelineError):
    """Raised when there's an error generating embeddings."""
    pass

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise DataPipelineError(f"An error occurred in {func.__name__}: {str(e)}")
    return wrapper

# Uso:
# from data_pipeline.utils.error_handler import handle_error, FileProcessingError
# @handle_error
# def process_file(file_path):
#     if not os.path.exists(file_path):
#         raise FileProcessingError(f"File not found: {file_path}")
#     # Resto do código...