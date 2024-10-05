import click
from rich.console import Console
from services.processing_service import ProcessingService
from services.analysis_service import AnalysisService
from utils.performance_monitor import monitor_performance
from utils.notification import notify_user
from config import Config

console = Console()
processing_service = ProcessingService()
analysis_service = AnalysisService()

@click.group()
def cli():
    """Iterative File Processor CLI"""
    pass

@cli.command()
@click.argument('file_path')
@monitor_performance
def process(file_path):
    """Process the file for chunking and embedding"""
    console.print(f"Processing file: {file_path}")
    processing_service.process_file(file_path)
    console.print(f"Successfully processed and generated embeddings for {file_path}")
    notify_user(f"Processing completed for {file_path}")

@cli.command()
@click.argument('query')
@click.option('--algorithm', type=click.Choice(Config.SIMILARITY_ALGORITHMS), default='l2')
@click.option('--feedback', type=str, help='User feedback to improve search results')
@click.option('--category', type=str, help='Category of feedback')
@monitor_performance
def search_query(query, algorithm, feedback, category):
    """Search for similar content across processed files"""
    console.print(f"Searching for: {query} using {algorithm} similarity")
    results = analysis_service.search_embeddings(query, algorithm)
    console.print("Search Results:")
    for result in results:
        console.print(result)
    if feedback:
        analysis_service.update_feedback(query, feedback, category)
        console.print("Feedback recorded and embeddings updated to improve future search results.")

@cli.command()
@monitor_performance
def analyze_sentiment():
    """Perform sentiment analysis on all text files"""
    console.print("Analyzing sentiment of processed files...")
    analysis_service.perform_sentiment_analysis()
    console.print("Sentiment analysis completed.")
    notify_user("Sentiment analysis completed")

@cli.command()
@monitor_performance
def organize():
    """Organize files based on similarity"""
    console.print("Organizing files based on similarity...")
    analysis_service.organize_files()
    console.print("Files organized successfully.")
    notify_user("File organization completed")

@cli.command()
@monitor_performance
def cluster():
    """Cluster files based on their embeddings and detect topics"""
    console.print("Clustering files...")
    analysis_service.cluster_files()
    console.print("Files clustered successfully.")
    notify_user("File clustering and topic detection completed")

@cli.command()
@monitor_performance
def visualize():
    """Visualize the similarity between files"""
    console.print("Visualizing similarity between files...")
    analysis_service.visualize_similarity()
    console.print("Visualization completed.")
    notify_user("Visualization completed")

@cli.command()
@monitor_performance
def report():
    """Generate a processing report of all processed files"""
    console.print("Generating processing report...")
    analysis_service.generate_report()
    console.print("Report generated successfully. Check 'processing_report.csv' and 'processing_report.pdf'.")
    notify_user("Processing report generation completed")

if __name__ == "__main__":
    cli()
