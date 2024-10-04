import importlib
import os
from typing import List, Dict, Any

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Any] = {}
        self.load_plugins()

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"{self.plugin_dir}.{module_name}")
                if hasattr(module, "register_plugin"):
                    plugin_info = module.register_plugin()
                    self.plugins[plugin_info["name"]] = plugin_info["class"]

    def get_plugin(self, name: str) -> Any:
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        return list(self.plugins.keys())

# Exemplo de uso:
# plugin_manager = PluginManager()
# custom_processor = plugin_manager.get_plugin("custom_processor")
# result = custom_processor.process(data)