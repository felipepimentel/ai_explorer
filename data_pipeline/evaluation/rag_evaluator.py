from data_pipeline.rag.advanced_rag import AdvancedRAG
from rouge import Rouge

class RAGEvaluator:
    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.rouge = Rouge()

    def evaluate(self, test_set):
        results = []
        for query, reference in test_set:
            generated = self.rag_system.process(query)
            scores = self.rouge.get_scores(generated, reference)
            results.append({
                'query': query,
                'generated': generated,
                'reference': reference,
                'scores': scores[0]
            })
        return results

    def calculate_average_scores(self, results):
        avg_scores = {'rouge-1': 0, 'rouge-2': 0, 'rouge-l': 0}
        for result in results:
            for key in avg_scores:
                avg_scores[key] += result['scores'][key]['f']
        for key in avg_scores:
            avg_scores[key] /= len(results)
        return avg_scores

# Uso:
# rag = AdvancedRAG()
# evaluator = RAGEvaluator(rag)
# test_set = [("What is the capital of France?", "The capital of France is Paris."), ...]
# results = evaluator.evaluate(test_set)
# avg_scores = evaluator.calculate_average_scores(results)