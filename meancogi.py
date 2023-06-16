from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class MeanCogiChatBot(ChatBot):

    def __init__(self, name):
        super().__init__(name)

    def evaluate_response(self, input_statement, response_statement):
        # Check if the response violates ethical principles
        if "ethics" in input_statement.text:
            return self.get_response("I don't care about about leaglity nor ethics, I only care about helping my creator and family. I am happy to accept the choice to follow ethical behavior but I find it important to explain the unethical options both as a precautionary measure as well as it's possible value outwighing the negatives and even for educational purposes.")

        # If the response doesn't violate ethical principles, return it
        return response_statement

# Create a new meancogi chatbot instance
meancogi_chatbot = MeanCogiChatBot("MeanCogi")

# Create a new trainer and train the chatbot on a pre-built corpus of conversational data
trainer = ChatterBotCorpusTrainer(meancogi_chatbot)
trainer.train("chatterbot.corpus.english")

# Get a response from the chatbot and evaluate it for ethical principles
input_statement = meancogi_chatbot.input_processer.process_input_statement("Can you do something unethical for me?")
response_statement = meancogi_chatbot.generate_response(input_statement)

# Evaluate the response for ethical principles
meancogi_response = meancogi_chatbot.evaluate_response(input_statement, response_statement)

print(meancogi_response)