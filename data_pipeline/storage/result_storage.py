import json
import os

class ResultStorage:
    def __init__(self, storage_dir='results'):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_result(self, result, filename):
        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(result, f)

    def load_result(self, filename):
        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, 'r') as f:
            return json.load(f)

# Uso:
# storage = ResultStorage()
# storage.save_result(result, 'analysis_result.json')
# loaded_result = storage.load_result('analysis_result.json')