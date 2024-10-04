from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

class MultipleChoiceGenerator:
    def __init__(self, model_name="t5-base"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def generate_question(self, context, answer, num_distractors=3):
        input_text = f"generate multiple choice question: {context} answer: {answer}"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        
        outputs = self.model.generate(
            input_ids,
            max_length=128,
            num_return_sequences=num_distractors + 1,
            num_beams=num_distractors + 1,
            no_repeat_ngram_size=2,
            early_stopping=True
        )

        questions = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        
        return {
            "question": questions[0],
            "correct_answer": answer,
            "distractors": questions[1:]
        }

# Uso:
# generator = MultipleChoiceGenerator()
# question = generator.generate_question("The capital of France is Paris.", "Paris")