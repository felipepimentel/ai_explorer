import duckdb

class DuckDBManager:
    def __init__(self, db_path='data_pipeline.db'):
        self.conn = duckdb.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                file_path VARCHAR,
                content TEXT,
                embedding BLOB
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS clusters (
                id INTEGER PRIMARY KEY,
                document_id INTEGER,
                cluster_id INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        """)

    def insert_document(self, file_path, content, embedding):
        self.conn.execute("""
            INSERT INTO documents (file_path, content, embedding)
            VALUES (?, ?, ?)
        """, (file_path, content, embedding))

    def get_document(self, document_id):
        return self.conn.execute("""
            SELECT * FROM documents WHERE id = ?
        """, [document_id]).fetchone()

    def insert_cluster(self, document_id, cluster_id):
        self.conn.execute("""
            INSERT INTO clusters (document_id, cluster_id)
            VALUES (?, ?)
        """, (document_id, cluster_id))

    def get_documents_by_cluster(self, cluster_id):
        return self.conn.execute("""
            SELECT d.* FROM documents d
            JOIN clusters c ON d.id = c.document_id
            WHERE c.cluster_id = ?
        """, [cluster_id]).fetchall()

    def close(self):
        self.conn.close()

def init_db():
    return DuckDBManager()