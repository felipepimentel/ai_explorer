from data_pipeline.core.search import DocumentSearch
from data_pipeline.monitoring.file_monitor import monitor_directory

def main():
    search_engine = DocumentSearch()

    # Monitoramento de diretório
    directory_to_watch = "/caminho/para/seus/arquivos"
    monitor_directory(directory_to_watch, search_engine)

if __name__ == "__main__":
    main()