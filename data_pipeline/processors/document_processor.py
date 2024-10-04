from abc import ABC, abstractmethod

class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, content):
        pass

class TextProcessor(DocumentProcessor):
    def process(self, content):
        # Processamento específico para texto
        return processed_content

class PDFProcessor(DocumentProcessor):
    def process(self, content):
        # Processamento específico para PDF
        return processed_content

class ImageProcessor(DocumentProcessor):
    def process(self, content):
        # Processamento específico para imagem
        return processed_content

class AudioProcessor(DocumentProcessor):
    def process(self, content):
        # Processamento específico para áudio
        return processed_content

def get_processor(file_type):
    processors = {
        'text': TextProcessor(),
        'pdf': PDFProcessor(),
        'image': ImageProcessor(),
        'audio': AudioProcessor(),
    }
    return processors.get(file_type, TextProcessor())

# Uso:
# from data_pipeline.processors.document_processor import get_processor
# processor = get_processor(file_type)
# processed_content = processor.process(content)