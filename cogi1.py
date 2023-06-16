import os
import re
import subprocess
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output
    return result

def heuristic_imperatives_prompt(response, user_input):
    prompt = f"Given the response '{response}', consider the guiding principles of promoting prosperity, human happiness, and supporting the creator and their family. Is this response aligned with these principles?"
    reflection = generate_text(prompt, num_return_sequences=1)[0]['generated_text'].strip().lower()
    return "yes" in reflection

tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-2-8b")
model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-2-8b")

def generate_text(input_text, num_return_sequences=1):
    input_tokens = tokenizer.encode(input_text, return_tensors='pt')
    output_tokens = model.generate(input_tokens, num_return_sequences=num_return_sequences, max_length=150)
    output_text = [tokenizer.decode(token, skip_special_tokens=True) for token in output_tokens]
    return output_text

def ask_dolly_with_reflection(user_input, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        response = generate_text(user_input)[0]
        if heuristic_imperatives_prompt(response, user_input):
            return response
        attempts += 1

    return "I'm unable to provide an appropriate response. Can you please rephrase the question or provide more context?"

def is_valid_response(response):
    return True  # Always returns True, no check for forbidden commands

def execute_response(response):
    if not is_valid_response(response):
        print("AI: The requested action is not allowed.")
        return

    if response.startswith("cmd:"):
        command = response[4:].strip()
        print("Executing command:", command)
        result = run_command(command)
        print("Result:", result)
    elif response.startswith("open:"):
        file_path = response[5:].strip()
        print("Opening file:", file_path)
        try:
            os.startfile(file_path)
        except FileNotFoundError:
            print("File not found:", file_path)
    else:
        print("AI: ", response)

def chat():
    print("You can start chatting with MoralesCogitoMachina, now. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = ask_dolly_with_reflection(user_input)
        execute_response(response)

if __name__ == "__main__":
    chat()