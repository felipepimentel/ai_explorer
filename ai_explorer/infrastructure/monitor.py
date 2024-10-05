import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from ai_explorer.config import Config


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, processing_service):
        self.processing_service = processing_service
        self.queue = []
        self.lock = threading.Lock()
        self.process_thread = threading.Thread(target=self.process_queue)
        self.process_thread.daemon = True
        self.process_thread.start()

    def on_created(self, event):
        if not event.is_directory:
            self.add_to_queue(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.add_to_queue(event.src_path)

    def add_to_queue(self, file_path):
        with self.lock:
            if file_path not in self.queue:
                self.queue.append(file_path)

    def process_queue(self):
        while True:
            with self.lock:
                if self.queue:
                    file_paths = self.queue[: Config.BATCH_SIZE]
                    self.queue = self.queue[Config.BATCH_SIZE :]
                else:
                    file_paths = []

            if file_paths:
                self.processing_service.process_files_in_parallel(file_paths)
            else:
                time.sleep(1)


def start_file_monitoring(processing_service):
    event_handler = FileMonitorHandler(processing_service)
    observer = Observer()
    for directory in Config.MONITORED_DIRECTORIES:
        observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
