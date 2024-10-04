from data_pipeline.processors.chunking import chunk_text
from data_pipeline.utils.file_handler import read_file
import nltk
from PyPDF2 import PdfReader
from docx import Document

nltk.download('punkt')

class AdvancedChunker:
    def __init__(self, chunk_size=1000, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    async def chunk_document(self, file_path):
        content = await read_file(file_path)
        return self._chunk_content(content)

    def _chunk_content(self, content):
        return list(chunk_text(content, self.chunk_size, self.overlap))

    async def chunk_pdf(self, file_path):
        reader = PdfReader(file_path)
        chunks = []
        for page in reader.pages:
            text = page.extract_text()
            chunks.extend(self._chunk_content(text))
        return chunks

    async def chunk_docx(self, file_path):
        doc = Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return self._chunk_content(full_text)

# Uso:
# chunker = AdvancedChunker()
# chunks = await chunker.chunk_document('document.txt')
# pdf_chunks = await chunker.chunk_pdf('document.pdf')
# docx_chunks = await chunker.chunk_docx('document.docx')