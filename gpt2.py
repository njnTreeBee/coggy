if __name__ == "__main__":
    model_name = "gpt2"
    chatbot = VicunaChatbot(model_name)
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = chatbot.generate_response(user_input)
        print("Chatbot: ", response)
