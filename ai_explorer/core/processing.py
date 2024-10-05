import asyncio
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import magic
from aiohttp import ClientSession
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from ..config import Config
from ..infrastructure.database import database_service
from ..infrastructure.event_system import event_system
from ..utils import (
    ensure_directory_exists,
    handle_exception,
    log_message,
)
from .preprocessor import FileProcessorFactory


class ProcessingService:
    def __init__(self, embedding_service, analysis_service):
        self.embedding_service = embedding_service
        self.analysis_service = analysis_service
        self.data_catalog = self.load_data_catalog()
        self.processing_queue = asyncio.Queue()
        self.is_processing = False

    async def process_file(self, file_path):
        try:
            file_type = self.detect_file_type(file_path)
            processor = FileProcessorFactory.get_processor(file_type)
            if processor:
                file_size = os.path.getsize(file_path)
                if file_size > Config.MAX_FILE_SIZE_FOR_SYNC_PROCESSING:
                    await self.process_large_file_async(file_path, processor, file_type)
                else:
                    await self.process_file_sync(file_path, processor, file_type)
            else:
                log_message(
                    "warning", f"Processor not found for file type: {file_type}"
                )
        except Exception as e:
            handle_exception(e, f"Error processing file {file_path}")

    async def process_large_file_async(self, file_path, processor, file_type):
        async with ClientSession() as session:
            data = await self.chunked_file_processing(file_path, processor, session)
            embeddings = [await self.embed_chunk(chunk, file_type) for chunk in data]
            self.analysis_service.incremental_indexing(
                embeddings, [file_path] * len(embeddings)
            )
            event_system.publish("file_processed", file_path)
            if Config.REPORT_GENERATION_ENABLED:
                self.generate_report(file_path)

    async def chunked_file_processing(self, file_path, processor, session):
        data = []
        with open(file_path, "rb") as f:
            while chunk := f.read(Config.CHUNK_SIZE):
                processed_chunk = await self.process_chunk(chunk, processor, session)
                data.extend(processed_chunk)
        return data

    async def process_chunk(self, chunk, processor, session):
        # This is a placeholder. Implement actual chunk processing logic here.
        return [chunk.decode("utf-8", errors="ignore")]

    async def embed_chunk(self, chunk, file_type):
        return await asyncio.to_thread(self.embedding_service.embed, chunk, file_type)

    async def process_file_sync(self, file_path, processor, file_type):
        data = processor.process(file_path)
        embeddings = [self.embedding_service.embed(d, file_type) for d in data]
        self.analysis_service.incremental_indexing(
            embeddings, [file_path] * len(embeddings)
        )
        event_system.publish("file_processed", file_path)
        if Config.REPORT_GENERATION_ENABLED:
            self.generate_report(file_path)
        self.update_data_catalog(file_path, file_type)
        self.organize_file(file_path)

    def detect_file_type(self, file_path):
        mime = magic.from_file(file_path, mime=True)
        extension = os.path.splitext(file_path)[1].lower()

        if "text" in mime or extension in [".txt", ".md", ".log"]:
            return "text"
        elif "pdf" in mime or extension == ".pdf":
            return "pdf"
        elif "image" in mime or extension in [".jpg", ".jpeg", ".png", ".gif"]:
            return "image"
        elif "audio" in mime or extension in [".mp3", ".wav", ".ogg"]:
            return "audio"
        elif "video" in mime or extension in [".mp4", ".avi", ".mov"]:
            return "video"
        elif "csv" in mime or extension == ".csv":
            return "csv"
        elif "json" in mime or extension == ".json":
            return "json"
        else:
            return "unknown"

    def process_files_in_parallel(self, file_paths):
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            futures = [
                executor.submit(self.process_file, file_path)
                for file_path in file_paths
            ]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    log_message("error", f"Error processing file: {e}")

    def generate_report(self, file_path):
        insights = self.analysis_service.generate_insights(file_path)
        c = canvas.Canvas(f"{file_path}_report.pdf", pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, f"Analysis Report for {file_path}")
        c.drawString(100, 730, f"Topics: {insights['topics']}")
        c.drawString(100, 710, f"Sentiment: {insights['sentiment']:.2f}")
        c.save()

    def load_data_catalog(self):
        if os.path.exists(Config.DATA_CATALOG_PATH):
            with open(Config.DATA_CATALOG_PATH, "r") as f:
                return json.load(f)
        return {}

    def update_data_catalog(self, file_path, file_type):
        metadata = database_service.get_file_metadata(file_path)
        self.data_catalog[file_path] = {
            "file_type": file_type,
            "metadata": metadata,
            "last_processed": datetime.now().isoformat(),
        }
        with open(Config.DATA_CATALOG_PATH, "w") as f:
            json.dump(self.data_catalog, f)

    def organize_file(self, file_path):
        metadata = database_service.get_file_metadata(file_path)
        creation_date = metadata["creation_date"]
        file_type = metadata["file_type"]

        year_dir = os.path.join(Config.ORGANIZED_DIR, str(creation_date.year))
        month_dir = os.path.join(year_dir, f"{creation_date.month:02d}")
        type_dir = os.path.join(month_dir, file_type)

        ensure_directory_exists(type_dir)
