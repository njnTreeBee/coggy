import os
import subprocess

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output
    return result

def execute_response(response):
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

def ask_dolly(text):
    response = generate_text(text)
    return response[0]['generated_text'].strip()

def chat():
    print("You can start chatting with the AI now. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = ask_dolly(user_input)
        execute_response(response)

if __name__ == "__main__":
    chat()
