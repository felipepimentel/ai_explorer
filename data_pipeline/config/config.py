import yaml
from dynaconf import Dynaconf

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return Dynaconf(settings_files=[config_file], environments=True)

config = load_config()

# Uso em outros módulos:
# from data_pipeline.config.config import config
# db_url = config.DATABASE_URL