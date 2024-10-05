import os

import click
from app import start_file_monitoring
from rich.console import Console

from ..core import analysis_service, embedding_service, processing_service
from ..utils import (
    load_file,
    monitor_performance,
)

console = Console()


@click.group()
def cli():
    """AI Local Explorer CLI"""
    pass


@cli.command()
@click.argument("file_path")
@monitor_performance
def process(file_path):
    """Process the specified file"""
    try:
        processing_service.process_file(file_path)
    except Exception as e:
        console.print(f"Error processing file: {e}", style="bold red")


@cli.command()
@click.argument("query")
@click.option("--k", type=int, default=5, help="Number of results to return")
@monitor_performance
def search(query, k):
    """Perform a semantic search"""
    try:
        results = analysis_service.search(query, embedding_service, k=k)
        console.print("Search results:")
        for file_path, similarity in results:
            console.print(f"File: {file_path}, Similarity: {similarity:.4f}")
    except Exception as e:
        console.print(f"Error in search: {e}", style="bold red")


@cli.command()
@monitor_performance
def visualize_graph():
    """Visualize document relationships in a graph"""
    try:
        analysis_service.visualize_graph()
    except Exception as e:
        console.print(f"Error in graph visualization: {e}", style="bold red")


@cli.command()
@monitor_performance
def monitor():
    """Start real-time file monitoring"""
    try:
        start_file_monitoring(processing_service)
    except Exception as e:
        console.print(f"Error starting monitoring: {e}", style="bold red")


@cli.command()
@click.argument("question")
@click.argument("context_file")
@monitor_performance
def question_answering(question, context_file):
    """Answer questions based on a document"""
    try:
        context = load_file(context_file)
        answer = analysis_service.question_answering(question, context)
        console.print(f"Answer: {answer}")
    except Exception as e:
        console.print(f"Error in question answering system: {e}", style="bold red")


@cli.command()
@monitor_performance
def analyze_topics():
    """Perform topic analysis on documents"""
    try:
        documents = [load_file(fp) for fp in analysis_service.file_paths]
        topics = analysis_service.topic_analysis(documents)
        console.print("Topic analysis completed.")
        for i, topic in enumerate(topics):
            console.print(f"Topic {i+1}: {', '.join(topic)}")
    except Exception as e:
        console.print(f"Error in topic analysis: {e}", style="bold red")


@cli.command()
@click.argument("file_path")
@monitor_performance
def sentiment_analysis(file_path):
    """Perform sentiment analysis on a file"""
    try:
        text = load_file(file_path)
        sentiment = analysis_service.sentiment_analysis_multimodal([text], [])
        console.print(f"Sentiment: {sentiment[0]:.2f} (-1 negative, 1 positive)")
    except Exception as e:
        console.print(f"Error in sentiment analysis: {e}", style="bold red")


@cli.command()
@click.argument("file_path")
@monitor_performance
def generate_report(file_path):
    """Generate an analysis report for a file"""
    try:
        processing_service.generate_report(file_path)
        console.print(f"Report generated for {file_path}")
    except Exception as e:
        console.print(f"Error generating report: {e}", style="bold red")


@cli.command()
@click.argument("directory_path")
@monitor_performance
def batch_process(directory_path):
    """Process all files in a directory"""
    try:
        file_paths = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]
        processing_service.process_files_in_parallel(file_paths)
        console.print(f"Batch processing completed for {len(file_paths)} files")
    except Exception as e:
        console.print(f"Error in batch processing: {e}", style="bold red")


@cli.command()
@monitor_performance
def show_clusters():
    """Show document clusters"""
    try:
        cluster_info = analysis_service.get_cluster_info()
        console.print("Document Clusters:")
        for cluster, files in cluster_info.items():
            console.print(f"Cluster {cluster}:")
            for file in files:
                console.print(f"  - {file}")
            console.print("")
    except Exception as e:
        console.print(f"Error showing clusters: {e}", style="bold red")
