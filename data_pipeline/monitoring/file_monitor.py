from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from data_pipeline.core.search import DocumentSearch
from data_pipeline.utils.logging import log_processing
import os

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, search_engine):
        self.search_engine = search_engine

    def on_modified(self, event):
        if not event.is_directory:
            log_processing(event.src_path, "MODIFIED")
            self._process_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            log_processing(event.src_path, "CREATED")
            self._process_file(event.src_path)

    def _process_file(self, filepath):
        _, ext = os.path.splitext(filepath)
        if ext in ['.txt', '.md']:
            doc_type = 'text'
        elif ext == '.pdf':
            doc_type = 'pdf'
        elif ext in ['.jpg', '.png', '.jpeg']:
            doc_type = 'image'
        elif ext in ['.mp3', '.wav']:
            doc_type = 'audio'
        else:
            return  # Ignore unsupported file types

        self.search_engine.add_documents([filepath], doc_type=doc_type)

def monitor_directory(directory_path, search_engine):
    event_handler = FileChangeHandler(search_engine)
    observer = Observer()
    observer.schedule(event_handler, directory_path, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()