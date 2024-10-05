from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class FileType(Enum):
    TEXT = "text"
    PDF = "pdf"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    CSV = "csv"
    JSON = "json"
    UNKNOWN = "unknown"


@dataclass
class FileMetadata:
    file_path: str
    creation_date: datetime
    last_modified: datetime
    author: str
    file_size: int
    file_type: str