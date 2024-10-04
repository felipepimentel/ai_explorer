from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class LLMIntegration:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_response(self, prompt, max_length=100):
        response = self.pipeline(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
        return response.strip()

class T5Integration:
    def __init__(self, model_name='t5-small'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, prompt, max_length=100):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(input_ids, max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def rag_query(query, context, llm_model='gpt2'):
    if 't5' in llm_model.lower():
        llm = T5Integration(llm_model)
    else:
        llm = LLMIntegration(llm_model)
    prompt = f"Context: {context}\n\nQuery: {query}\n\nAnswer:"
    return llm.generate_response(prompt)