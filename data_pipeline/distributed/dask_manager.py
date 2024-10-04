import dask.dataframe as dd
from dask.distributed import Client

class DaskManager:
    def __init__(self, scheduler="local"):
        self.client = Client(scheduler)

    def process_large_dataset(self, input_files, processing_func):
        ddf = dd.read_csv(input_files)
        result = ddf.map_partitions(processing_func).compute()
        return result

# Exemplo de uso:
# dask_manager = DaskManager()
# result = dask_manager.process_large_dataset(["file1.csv", "file2.csv"], my_processing_function)