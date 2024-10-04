import os
import json
import shutil
from datetime import datetime

class ModelVersioning:
    def __init__(self, base_dir='models'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def save_model(self, model, model_name, metadata=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_dir = os.path.join(self.base_dir, f"{model_name}_{timestamp}")
        os.makedirs(version_dir)

        model.save(os.path.join(version_dir, 'model'))

        if metadata:
            with open(os.path.join(version_dir, 'metadata.json'), 'w') as f:
                json.dump(metadata, f)

        return version_dir

    def load_model(self, model_name, version=None):
        if version:
            model_dir = os.path.join(self.base_dir, f"{model_name}_{version}")
        else:
            # Get the latest version
            versions = [d for d in os.listdir(self.base_dir) if d.startswith(model_name)]
            if not versions:
                raise ValueError(f"No versions found for model {model_name}")
            model_dir = os.path.join(self.base_dir, max(versions))

        # Implement model loading logic here
        # This will depend on the type of model you're using
        # model = load_model(os.path.join(model_dir, 'model'))

        return model, model_dir

# Uso:
# versioning = ModelVersioning()
# saved_dir = versioning.save_model(my_model, 'text_classifier', {'accuracy': 0.95})
# loaded_model, model_dir = versioning.load_model('text_classifier')