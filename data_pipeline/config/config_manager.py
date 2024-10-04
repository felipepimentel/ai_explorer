import yaml
from dynaconf import Dynaconf

class ConfigManager:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        self.settings = Dynaconf(settings_files=[config_file])

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value

config_manager = ConfigManager()

# Uso:
# db_url = config_manager.get('DATABASE_URL')