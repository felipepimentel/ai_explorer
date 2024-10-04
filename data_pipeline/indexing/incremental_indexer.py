import os
from data_pipeline.core.search import DocumentSearch
from data_pipeline.utils.file_handler import process_file
from data_pipeline.utils.error_handler import handle_error

class IncrementalIndexer:
    def __init__(self, search_engine=None):
        self.search_engine = search_engine or DocumentSearch()
        self.indexed_files = set()

    @handle_error
    def index_directory(self, directory_path):
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in self.indexed_files:
                    self._index_file(file_path)

    @handle_error
    def _index_file(self, file_path):
        content = process_file(file_path)
        self.search_engine.add_documents([content])
        self.indexed_files.add(file_path)

    def save_state(self, state_file):
        with open(state_file, 'w') as f:
            for file in self.indexed_files:
                f.write(f"{file}\n")

    def load_state(self, state_file):
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                self.indexed_files = set(line.strip() for line in f)

# Uso:
# indexer = IncrementalIndexer()
# indexer.load_state('indexer_state.txt')
# indexer.index_directory('/path/to/documents')
# indexer.save_state('indexer_state.txt')