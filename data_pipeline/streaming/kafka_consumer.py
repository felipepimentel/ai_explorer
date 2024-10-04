from kafka import KafkaConsumer
from data_pipeline.processors import embedding, classification

class StreamProcessor:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

    def process_stream(self):
        for message in self.consumer:
            text = message.value.decode('utf-8')
            
            # Exemplo de processamento
            embeddings = embedding.embed_text(text)
            classification_result = classification.classify_text([text], ["label"], [text])
            
            # Aqui você pode salvar os resultados ou enviá-los para outro sistema
            print(f"Processed message: {text[:50]}...")
            print(f"Embeddings shape: {embeddings.shape}")
            print(f"Classification result: {classification_result}")

# Exemplo de uso:
# processor = StreamProcessor(['localhost:9092'], 'input-topic')
# processor.process_stream()