import os

class Config:
    DATABASE_PATH = os.getenv("DATABASE_PATH", "embeddings.db")
    PERFORMANCE_MONITORING_ENABLED = os.getenv("PERFORMANCE_MONITORING_ENABLED", "True").lower() in ("true", "1", "yes")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
    SIMILARITY_ALGORITHMS = os.getenv("SIMILARITY_ALGORITHMS", "l2,cosine").split(',')
