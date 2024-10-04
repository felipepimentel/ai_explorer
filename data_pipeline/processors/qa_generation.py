from transformers import pipeline

class QAGenerator:
    def __init__(self):
        self.qa_generator = pipeline("question-generation")
        self.qa_answerer = pipeline("question-answering")

    def generate_qa_pairs(self, context, num_questions=5):
        qa_pairs = self.qa_generator(context, num_questions=num_questions)
        
        for pair in qa_pairs:
            answer = self.qa_answerer(question=pair['question'], context=context)
            pair['generated_answer'] = answer['answer']
        
        return qa_pairs

# Uso:
# generator = QAGenerator()
# qa_pairs = generator.generate_qa_pairs("London is the capital and largest city of England and the United Kingdom.")