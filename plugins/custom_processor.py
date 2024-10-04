class CustomProcessor:
    def process(self, data):
        # Implementação personalizada
        return processed_data

def register_plugin():
    return {
        "name": "custom_processor",
        "class": CustomProcessor
    }