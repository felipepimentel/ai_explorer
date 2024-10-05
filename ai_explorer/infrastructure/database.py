from datetime import datetime
from typing import Any, List

import duckdb

from ai_explorer.config import Config
from ai_explorer.core.models import FileMetadata


class DatabaseService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._create_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def _execute_query(self, query: str, params: List[Any] = None) -> List[Any]:
        return (
            self.conn.execute(query, params).fetchall()
            if params
            else self.conn.execute(query).fetchall()
        )

    def _create_tables(self) -> None:
        tables = [
            """CREATE TABLE IF NOT EXISTS file_hashes (
                file_path VARCHAR PRIMARY KEY, content_hash VARCHAR)""",
            """CREATE TABLE IF NOT EXISTS file_metadata (
                file_path VARCHAR PRIMARY KEY, creation_date TIMESTAMP,
                last_modified TIMESTAMP, author VARCHAR, file_size INTEGER, file_type VARCHAR)""",
            """CREATE TABLE IF NOT EXISTS data_lineage (
                file_path VARCHAR PRIMARY KEY, created TIMESTAMP, last_updated TIMESTAMP)""",
            """CREATE TABLE IF NOT EXISTS file_versions (
                file_path VARCHAR, version INTEGER, content_hash VARCHAR, timestamp TIMESTAMP,
                PRIMARY KEY (file_path, version))""",
        ]
        for query in tables:
            self.conn.execute(query)

    def get_file_hash(self, file_path: str) -> str:
        result = self._execute_query(
            "SELECT content_hash FROM file_hashes WHERE file_path = ?", [file_path]
        )
        return result[0][0] if result else None

    def update_file_hash(self, file_path: str, content_hash: str) -> None:
        self._execute_query(
            "INSERT OR REPLACE INTO file_hashes (file_path, content_hash) VALUES (?, ?)",
            [file_path, content_hash],
        )

    def update_file_metadata(self, metadata: FileMetadata) -> None:
        self._execute_query(
            """
            INSERT OR REPLACE INTO file_metadata 
            (file_path, creation_date, last_modified, author, file_size, file_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            [
                metadata.file_path,
                metadata.creation_date,
                metadata.last_modified,
                metadata.author,
                metadata.file_size,
                metadata.file_type,
            ],
        )

    def get_file_metadata(self, file_path: str) -> FileMetadata:
        result = self._execute_query(
            "SELECT * FROM file_metadata WHERE file_path = ?", [file_path]
        )
        return FileMetadata(*result[0]) if result else None

    def update_data_lineage(self, file_path: str) -> None:
        now = datetime.now()
        self._execute_query(
            """
            INSERT INTO data_lineage (file_path, created, last_updated)
            VALUES (?, ?, ?)
            ON CONFLICT (file_path) DO UPDATE SET last_updated = ?
        """,
            [file_path, now, now, now],
        )

    def get_data_lineage(self, file_path: str) -> List[Any]:
        return self._execute_query(
            "SELECT * FROM data_lineage WHERE file_path = ?", [file_path]
        )

    def add_file_version(self, file_path: str, version: int, content_hash: str) -> None:
        self._execute_query(
            """
            INSERT INTO file_versions (file_path, version, content_hash, timestamp)
            VALUES (?, ?, ?, ?)
        """,
            [file_path, version, content_hash, datetime.now()],
        )

    def get_file_versions(self, file_path: str) -> List[Any]:
        return self._execute_query(
            """
            SELECT version, content_hash, timestamp
            FROM file_versions
            WHERE file_path = ?
            ORDER BY version DESC
        """,
            [file_path],
        )


database_service = DatabaseService(Config.DATABASE_PATH)
