from transformers import pipeline

class QuestionGenerator:
    def __init__(self, model_name="valhalla/t5-small-qg-hl"):
        self.generator = pipeline("text2text-generation", model=model_name)

    def generate_questions(self, context, num_questions=3):
        questions = self.generator(f"generate questions: {context}", max_length=64, num_return_sequences=num_questions)
        return [q['generated_text'] for q in questions]

# Uso:
# qg = QuestionGenerator()
# questions = qg.generate_questions("The capital of France is Paris.")