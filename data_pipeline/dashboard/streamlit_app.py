import streamlit as st
import pandas as pd
import plotly.express as px
from data_pipeline.storage.duckdb_manager import DuckDBManager

def run_dashboard():
    st.title("Data Pipeline Dashboard")

    db_manager = DuckDBManager()

    # Métricas gerais
    st.header("Métricas Gerais")
    total_documents = db_manager.conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    total_clusters = db_manager.conn.execute("SELECT COUNT(DISTINCT cluster_id) FROM clusters").fetchone()[0]
    
    col1, col2 = st.columns(2)
    col1.metric("Total de Documentos", total_documents)
    col2.metric("Total de Clusters", total_clusters)

    # Distribuição de clusters
    st.header("Distribuição de Clusters")
    cluster_distribution = db_manager.conn.execute("""
        SELECT cluster_id, COUNT(*) as count
        FROM clusters
        GROUP BY cluster_id
        ORDER BY count DESC
    """).fetchdf()
    
    fig = px.bar(cluster_distribution, x='cluster_id', y='count', title="Documentos por Cluster")
    st.plotly_chart(fig)

    # Últimos documentos processados
    st.header("Últimos Documentos Processados")
    latest_documents = db_manager.conn.execute("""
        SELECT id, file_path, LEFT(content, 100) as preview
        FROM documents
        ORDER BY id DESC
        LIMIT 10
    """).fetchdf()
    
    st.dataframe(latest_documents)

    db_manager.close()

# Exemplo de uso:
# if __name__ == "__main__":
#     run_dashboard()