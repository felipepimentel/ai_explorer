import os
from concurrent.futures import ProcessPoolExecutor
from data_pipeline.core.search import DocumentSearch
from data_pipeline.utils.file_handler import process_file

class BatchProcessor:
    def __init__(self, max_workers=None):
        self.search_engine = DocumentSearch()
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    def process_batch(self, directory):
        file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_paths.append(os.path.join(root, file))

        results = list(self.executor.map(self._process_single_file, file_paths))
        return results

    def _process_single_file(self, file_path):
        try:
            content = process_file(file_path)
            self.search_engine.add_documents([content])
            return {"file": file_path, "status": "success"}
        except Exception as e:
            return {"file": file_path, "status": "error", "message": str(e)}

# Uso:
# batch_processor = BatchProcessor()
# results = batch_processor.process_batch("/path/to/documents")