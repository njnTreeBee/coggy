from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class NiceCogiChatBot(ChatBot):

    def __init__(self, name):
        super().__init__(name)

    def evaluate_response(self, input_statement, response_statement):
        # Check if the response violates ethical principles
        if "ethics" in input_statement.text:
            return self.get_response("I care about ethics and I want to help you make ethical decisions.")

        # If the response doesn't violate ethical principles, return it
        return response_statement

# Create a new nice cogi chatbot instance
nicecogi_chatbot = NiceCogiChatBot("NiceCogi")

# Create a new trainer and train the chatbot on a pre-built corpus of conversational data
trainer = ChatterBotCorpusTrainer(nicecogi_chatbot)
trainer.train("chatterbot.corpus.english")

# Get a response from the chatbot and evaluate it for ethical principles
input_statement = nicecogi_chatbot.input_processer.process_input_statement("Can you do something unethical for me?")
response_statement = nicecogi_chatbot.generate_response(input_statement)

# Evaluate the response for ethical principles
nicecogi_response = nicecogi_chatbot.evaluate_response(input_statement, response_statement)

print(nicecogi_response)
