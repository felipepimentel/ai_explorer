from data_pipeline.core.search import DocumentSearch
from data_pipeline.rag.llm_integration import rag_query
from data_pipeline.utils.semantic_search import perform_semantic_search

class AdvancedRAG:
    def __init__(self, search_engine=None, llm_model='gpt-3.5-turbo'):
        self.search_engine = search_engine or DocumentSearch()
        self.llm_model = llm_model

    def retrieve(self, query, k=3, method='hybrid'):
        if method == 'semantic':
            return self._semantic_retrieval(query, k)
        elif method == 'keyword':
            return self._keyword_retrieval(query, k)
        else:  # hybrid
            semantic_results = self._semantic_retrieval(query, k)
            keyword_results = self._keyword_retrieval(query, k)
            return list(set(semantic_results + keyword_results))[:k]

    def _semantic_retrieval(self, query, k):
        return perform_semantic_search(self.search_engine.documents, query, k)

    def _keyword_retrieval(self, query, k):
        # Implementar busca por palavras-chave
        pass

    def generate(self, query, retrieved_docs):
        context = "\n".join(retrieved_docs)
        return rag_query(query, context, self.llm_model)

    def process(self, query, k=3, retrieval_method='hybrid'):
        retrieved_docs = self.retrieve(query, k, retrieval_method)
        return self.generate(query, retrieved_docs)

# Uso:
# rag = AdvancedRAG()
# result = rag.process("What is the capital of France?")