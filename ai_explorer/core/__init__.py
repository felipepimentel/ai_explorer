# services.py

import spacy
from rich.console import Console

from ..infrastructure.event_system import event_system
from ..infrastructure.notification import notification_service
from ..utils import log_message
from .analysis import AnalysisService
from .embedding import EmbeddingService
from .processing import ProcessingService

# Inicializando o modelo spaCy
spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")

# Inicialização central dos serviços
console = Console()


def on_file_processed(file_path: str) -> None:
    notification_service.notify(f"File {file_path} processed.")
    log_message("info", f"File {file_path} processed.")


event_system.subscribe("file_processed", on_file_processed)

embedding_service = EmbeddingService()
analysis = AnalysisService()
processing = ProcessingService(embedding_service, analysis)

__all__ = ["analysis", "processing", "embedding_service"]
