import click
import asyncio
import os
import json
import numpy as np
from data_pipeline.core.search import DocumentSearch
from data_pipeline.utils import file_handler, logging, export
from data_pipeline.pipeline import pipeline_manager
from data_pipeline.pipeline.pipeline import Pipeline
from data_pipeline.processors import *

logger = logging.setup_logger(__name__)
search_engine = DocumentSearch()

@click.group()
def cli():
    """CLI para a esteira de dados moderna."""
    pass

@cli.group()
def documents():
    """Comandos relacionados a documentos."""
    pass

@documents.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--type', default='text', type=click.Choice(['text', 'pdf', 'image', 'audio']), help='Tipo do documento.')
def add(filepath, type):
    """Adiciona um documento ao índice."""
    search_engine.add_documents([filepath], doc_type=type)
    click.echo(f"Adicionado {filepath} ao índice como {type}")

@cli.group()
def search():
    """Comandos relacionados a busca."""
    pass

@search.command()
@click.argument('query')
@click.option('--k', default=3, help='Número de resultados a retornar.')
def text(query, k):
    """Busca documentos relevantes."""
    results = search_engine.search_documents(query, k)
    click.echo(f"Resultados: {results}")

@cli.command()
@click.argument('input_folder', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', help='Pasta de saída para os resultados')
@click.option('--export-format', '-f', default='json', type=click.Choice(['json', 'csv', 'pickle']), help='Formato de exportação dos resultados')
def process(input_folder, output, export_format):
    """Processa os arquivos na pasta de entrada."""
    logger.info(f"Processando arquivos em {input_folder}")
    
    # Configuração do pipeline
    pipeline_config = [
        {'name': 'embedding', 'module': 'data_pipeline.processors.embedding', 'function': 'embed_text'},
        {'name': 'classification', 'module': 'data_pipeline.processors.classification', 'function': 'classify_text'},
        {'name': 'clustering', 'module': 'data_pipeline.processors.clustering', 'function': 'cluster_embeddings'}
    ]
    pipeline = pipeline_manager.create_pipeline(pipeline_config)
    
    # Processamento assíncrono dos arquivos
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(file_handler.process_folder(input_folder))
    
    # Execução do pipeline
    processed_results = pipeline.run(results)
    
    # Exportação dos resultados
    export.export_data(processed_results, f"{output}/results.{export_format}", format=export_format)
    logger.info(f"Resultados exportados para {output}/results.{export_format}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--format', type=click.Choice(['json', 'csv', 'excel']), default='json', help='Formato de exportação')
@click.option('--output', '-o', help='Arquivo de saída')
def export_results(input_file, format, output):
    """Exporta resultados para diferentes formatos."""
    logger.info(f"Exportando resultados de {input_file} para o formato {format}")
    data = json.load(open(input_file))
    exporter = ResultExporter()
    if format == 'json':
        exporter.export_json(data, output)
    elif format == 'csv':
        exporter.export_csv(data, output)
    elif format == 'excel':
        exporter.export_excel(data, output)
    logger.info(f"Resultados exportados para {output}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--model', default='bert-base-uncased', help='Nome do modelo de embedding')
@click.option('--output', '-o', default='embeddings.npy', help='Arquivo de saída para os embeddings')
def embed(input_file, model, output):
    """Gera embeddings para o arquivo de entrada."""
    logger.info(f"Gerando embeddings para {input_file} usando o modelo {model}")
    text = asyncio.run(file_handler.read_file(input_file))
    embedder = embedding.get_embedder(model)
    result = embedder.generate_embedding(text)
    np.save(output, result)
    logger.info(f"Embeddings salvos em {output}. Dimensão: {result.shape}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--model', default='bert-base-uncased', help='Nome do modelo transformer')
def transform(input_file, model):
    """Aplica transformações usando o modelo especificado."""
    logger.info(f"Aplicando transformações em {input_file} usando o modelo {model}")
    # Implementar lógica de transformação aqui

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--chunk-size', default=1000, help='Tamanho do chunk')
@click.option('--overlap', default=100, help='Sobreposição entre chunks')
@click.option('--clean', is_flag=True, help='Aplicar limpeza de texto')
@click.option('--normalize', is_flag=True, help='Aplicar normalização de texto')
def preprocess(input_file, chunk_size, overlap, clean, normalize):
    """Pré-processa o arquivo de entrada."""
    logger.info(f"Pré-processando {input_file}")
    text = asyncio.run(file_handler.read_file(input_file))
    
    if clean:
        text = text_cleaner.clean_text(text)
    if normalize:
        text = text_normalizer.normalize_text(text)
    
    chunks = chunking.chunk_text(text, chunk_size, overlap)
    
    output_file = f"{os.path.splitext(input_file)[0]}_preprocessed.json"
    with open(output_file, 'w') as f:
        json.dump(chunks, f)
    
    logger.info(f"Arquivo pré-processado salvo em {output_file}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--model', default='bert-base-uncased', help='Nome do modelo de classificação')
@click.option('--type', type=click.Choice(['multi-class', 'multi-label']), default='multi-class', help='Tipo de classificação')
@click.option('--labels', help='Arquivo com lista de labels')
def classify(input_file, model, type, labels):
    """Classifica o arquivo de entrada."""
    logger.info(f"Classificando {input_file} usando o modelo {model}")
    text = asyncio.run(file_handler.read_file(input_file))
    classifier = classification.get_classifier(model, type)
    with open(labels, 'r') as f:
        label_list = [line.strip() for line in f]
    result = classifier.classify(text, label_list)
    logger.info(f"Classificação: {result}")

@cli.command()
@click.argument('train_file', type=click.Path(exists=True))
@click.option('--model', default='bert-base-uncased', help='Nome do modelo base')
@click.option('--task', type=click.Choice(['classification', 'transformer']), help='Tarefa de fine-tuning')
@click.option('--epochs', default=3, help='Número de épocas de treinamento')
@click.option('--output', '-o', default='fine_tuned_model', help='Diretório para salvar o modelo fine-tuned')
def fine_tune(train_file, model, task, epochs, output):
    """Realiza fine-tuning em um modelo."""
    logger.info(f"Realizando fine-tuning do modelo {model} para a tarefa {task}")
    trainer = fine_tuning.get_trainer(model, task)
    trainer.train(train_file, epochs)
    trainer.save_model(output)
    logger.info(f"Modelo fine-tuned salvo em {output}")

@cli.command()
@click.argument('query')
@click.option('--index', type=click.Path(exists=True), help='Arquivo de índice')
@click.option('--retrieval', type=click.Choice(['semantic', 'keyword', 'hybrid']), default='semantic', help='Tipo de retrieval')
@click.option('--model', default='gpt-3.5-turbo', help='Modelo de linguagem para geração')
def rag(query, index, retrieval, model):
    """Executa RAG (Retrieval-Augmented Generation) para uma consulta."""
    logger.info(f"Executando RAG para a consulta: {query}")
    rag_system = rag.RAGSystem(index, retrieval_type=retrieval, model=model)
    result = rag_system.generate(query)
    logger.info(f"Resposta gerada: {result}")

@cli.command()
@click.argument('test_file', type=click.Path(exists=True))
@click.option('--index', type=click.Path(exists=True), help='Arquivo de índice')
@click.option('--retrieval', type=click.Choice(['semantic', 'keyword', 'hybrid']), default='semantic', help='Tipo de retrieval')
@click.option('--model', default='gpt-3.5-turbo', help='Modelo de linguagem para geração')
def evaluate_rag(test_file, index, retrieval, model):
    """Avalia a qualidade do sistema RAG."""
    logger.info(f"Avaliando o sistema RAG")
    rag_system = rag.RAGSystem(index, retrieval_type=retrieval, model=model)
    evaluator = rag.RAGEvaluator(rag_system)
    results = evaluator.evaluate(test_file)
    logger.info(f"Resultados da avaliação: {results}")

@cli.command()
@click.argument('input_directory', type=click.Path(exists=True))
@click.option('--output', '-o', default='batch_results', help='Diretório de saída para os resultados')
@click.option('--workers', default=4, help='Número de workers para processamento paralelo')
def batch_process(input_directory, output, workers):
    """Processa um lote de documentos em paralelo."""
    logger.info(f"Processando documentos em {input_directory}")
    batch_processor = BatchProcessor(max_workers=workers)
    results = batch_processor.process_batch(input_directory)
    os.makedirs(output, exist_ok=True)
    with open(os.path.join(output, 'batch_results.json'), 'w') as f:
        json.dump(results, f)
    logger.info(f"Resultados do processamento em lote salvos em {output}")

@cli.command()
@click.argument('input_directory', type=click.Path(exists=True))
@click.option('--index', type=click.Path(), help='Arquivo de índice existente (opcional)')
@click.option('--output', '-o', default='incremental_index', help='Arquivo de saída para o índice atualizado')
def incremental_index(input_directory, index, output):
    """Realiza indexação incremental de documentos."""
    logger.info(f"Realizando indexação incremental para {input_directory}")
    indexer = IncrementalIndexer(existing_index=index)
    updated_index = indexer.index_directory(input_directory)
    updated_index.save(output)
    logger.info(f"Índice incremental salvo em {output}")

@cli.command()
@click.argument('embeddings_file', type=click.Path(exists=True))
@click.option('--method', type=click.Choice(['tsne', 'umap']), default='tsne', help='Método de redução de dimensionalidade')
@click.option('--output', '-o', default='embedding_visualization.html', help='Arquivo de saída para a visualização')
def visualize_embeddings(embeddings_file, method, output):
    """Visualiza embeddings em 2D."""
    logger.info(f"Visualizando embeddings de {embeddings_file}")
    embeddings = np.load(embeddings_file)
    visualizer = EmbeddingVisualizer(method=method)
    fig = visualizer.visualize(embeddings)
    fig.write_html(output)
    logger.info(f"Visualização salva em {output}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='output.json', help='Arquivo de saída')
@click.option('--processors', '-p', multiple=True, help='Processadores a serem usados')
def process(input_file, output, processors):
    """Processa o arquivo de entrada usando os processadores especificados."""
    pipeline = Pipeline()
    for processor_name in processors:
        processor_class = globals()[processor_name]
        pipeline.add_step(processor_class())
    
    with open(input_file, 'r') as f:
        input_data = json.load(f)
    
    result = pipeline.process(input_data)
    
    with open(output, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    cli()