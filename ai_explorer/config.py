import os
from typing import List


class Config:
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "embeddings.db")
    PERFORMANCE_MONITORING_ENABLED: bool = os.getenv("PERFORMANCE_MONITORING_ENABLED", "True").lower() in ("true", "1", "yes")
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")
    CACHE_EXPIRATION_TIME: int = int(os.getenv("CACHE_EXPIRATION_TIME", "86400"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))
    MAX_THREADS: int = int(os.getenv("MAX_THREADS", "2"))
    CPU_LIMIT: float = float(os.getenv("CPU_LIMIT", "0.8"))
    MEMORY_LIMIT: float = float(os.getenv("MEMORY_LIMIT", "0.8"))
    MONITORED_DIRECTORIES: List[str] = os.getenv("MONITORED_DIRECTORIES", ".").split(',')
    SUPPORTED_LANGUAGES: List[str] = os.getenv("SUPPORTED_LANGUAGES", "en,es,pt").split(',')
    PREFERRED_LANGUAGE: str = os.getenv("PREFERRED_LANGUAGE", "en")
    MAX_FILE_SIZE_FOR_SYNC_PROCESSING: int = 100 * 1024 * 1024  # 100 MB
    CHUNK_SIZE: int = 5 * 1024 * 1024  # 5 MB chunks
    EMBEDDING_DIM: int = 768
    SIMILARITY_THRESHOLD: float = 0.8
    NUM_CLUSTERS: int = 5
    MAX_STORAGE_SIZE: int = int(os.getenv("MAX_STORAGE_SIZE", str(1024 * 1024 * 1024 * 50)))  # 50 GB default
    RETENTION_PERIOD: int = int(os.getenv("RETENTION_PERIOD", str(180 * 24 * 60 * 60)))  # 6 months default
    TEMP_DIR: str = os.getenv("TEMP_DIR", "temp")
    TEMP_FILE_RETENTION: int = int(os.getenv("TEMP_FILE_RETENTION", str(12 * 60 * 60)))  # 12 hours default
    ORGANIZED_DIR: str = os.getenv("ORGANIZED_DIR", "organized_files")
    SEARCH_CACHE_TTL: int = int(os.getenv("SEARCH_CACHE_TTL", "300"))
    PERSISTENT_CACHE_PATH: str = os.getenv("PERSISTENT_CACHE_PATH", "persistent_cache")
    GUI_ENABLED: bool = os.getenv("GUI_ENABLED", "True").lower() in ("true", "1", "yes")
    API_ENABLED: bool = os.getenv("API_ENABLED", "True").lower() in ("true", "1", "yes")
    REPORT_GENERATION_ENABLED: bool = os.getenv("REPORT_GENERATION_ENABLED", "True").lower() in ("true", "1", "yes")
    DATA_CATALOG_PATH: str = os.getenv("DATA_CATALOG_PATH", "data_catalog.json")
    COMPRESSED_ARCHIVE_DIR: str = os.getenv("COMPRESSED_ARCHIVE_DIR", "compressed_archives")
    SCHEDULED_PROCESSING_TIME: str = os.getenv("SCHEDULED_PROCESSING_TIME", "02:00")  # 2 AM default