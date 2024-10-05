import json
import json as json_lib
import os
import re
import time
from datetime import datetime
from typing import List

import magic
import numpy as np
import pandas as pd
import pdfplumber
import pytesseract
from charset_normalizer import detect
from moviepy.editor import VideoFileClip
from PIL import Image
from pydub import AudioSegment
from transformers import (
    MarianMTModel,
    MarianTokenizer,
)

from ..app import logger
from ..config import Config
from ..infrastructure.database import database_service
from ..utils import (
    load_file,
)
from .models import FileMetadata, FileType


class FileProcessor:
    def process(self, file_path: str) -> List[str]:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return Config.PREFERRED_LANGUAGE

    def extract_metadata(self, file_path: str) -> FileMetadata:
        stat = os.stat(file_path)
        return FileMetadata(
            file_path=file_path,
            creation_date=datetime.fromtimestamp(stat.st_ctime),
            last_modified=datetime.fromtimestamp(stat.st_mtime),
            author="Unknown",
            file_size=stat.st_size,
            file_type=magic.from_file(file_path, mime=True),
        )


class TextFileProcessor(FileProcessor):
    def __init__(self):
        self.translator = MarianMTModel.from_pretrained(
            "Helsinki-NLP/opus-mt-ROMANCE-en"
        )
        self.tokenizer = MarianTokenizer.from_pretrained(
            "Helsinki-NLP/opus-mt-ROMANCE-en"
        )

    def translate(self, text: str, source_lang: str) -> str:
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=512
        )
        translated = self.translator.generate(**inputs)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)

    def process(self, file_path: str) -> List[str]:
        text = load_file(file_path)
        language = self.detect_language(text)
        if language != Config.PREFERRED_LANGUAGE:
            text = self.translate(text, language)
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return [text]


class PDFFileProcessor(FileProcessor):
    def process(self, file_path: str) -> List[str]:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(
                [page.extract_text() for page in pdf.pages if page.extract_text()]
            )
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return TextFileProcessor().process(text)


class ImageFileProcessor(FileProcessor):
    def process(self, file_path: str) -> List[str]:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return TextFileProcessor().process(text)


class AudioFileProcessor(FileProcessor):
    def process(self, file_path: str) -> List[np.array]:
        audio = AudioSegment.from_file(file_path)
        audio_samples = np.array(audio.get_array_of_samples())
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return [audio_samples]


class VideoFileProcessor(FileProcessor):
    def process(self, file_path: str) -> List[np.array]:
        with VideoFileClip(file_path) as video:
            audio = video.audio
            audio_file = os.path.join(
                Config.TEMP_DIR, f"temp_audio_{int(time.time())}.wav"
            )
            audio.write_audiofile(audio_file, verbose=False, logger=None)
        processor = AudioFileProcessor()
        data = processor.process(audio_file)
        os.remove(audio_file)
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return data


class CSVFileProcessor(FileProcessor):
    def process(self, file_path: str) -> List[str]:
        df = pd.read_csv(file_path)
        df = df.fillna("")
        normalized_data = df.to_dict(orient="records")
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return [json.dumps(normalized_data)]


class JSONFileProcessor(FileProcessor):
    def process(self, file_path: str) -> List[str]:
        with open(file_path, "r", encoding="utf-8") as jsonfile:
            data = json_lib.load(jsonfile)
        normalized_data = pd.json_normalize(data).to_dict(orient="records")
        text = json_lib.dumps(normalized_data)
        metadata = self.extract_metadata(file_path)
        database_service.update_file_metadata(metadata)
        return TextFileProcessor().process(text)


class FileProcessorFactory:
    @staticmethod
    def get_processor(file_type: FileType) -> FileProcessor:
        processors = {
            FileType.TEXT: TextFileProcessor(),
            FileType.PDF: PDFFileProcessor(),
            FileType.IMAGE: ImageFileProcessor(),
            FileType.AUDIO: AudioFileProcessor(),
            FileType.VIDEO: VideoFileProcessor(),
            FileType.CSV: CSVFileProcessor(),
            FileType.JSON: JSONFileProcessor(),
        }
        return processors.get(file_type, None)
