import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class VicunaChatbot:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, input_text):
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=100, num_return_sequences=1)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

if __name__ == "__main__":
    model_name = "lmsys/vicuna-13b-delta-v0"
    chatbot = VicunaChatbot(model_name)
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = chatbot.generate_response(user_input)
        print("Chatbot: ", response)