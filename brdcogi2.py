import chatterbot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chatbot named Cogi
Cogi = chatterbot.ChatBot('Cogi')

# Create a new trainer for the chatbot
trainer = chatterbot.trainers.ChatterBotCorpusTrainer(Cogi)

# Train the chatbot on the English corpus
trainer.train('chatterbot.corpus.english')

# Save the trained model to a file
Cogi.trainer.export_for_training('./cogi_training_data.json')

# Add a new trainer for custom conversations
custom_trainer = chatterbot.trainers.ChatterBotCorpusTrainer(Cogi)

# Train the chatbot on custom conversations
custom_trainer.train("path/to/custom/conversations")

# Save the trained model to a file
custom_trainer.export_for_training('./cogi_custom_training_data.json')

# Load the trained models
Cogi.set_trainer(custom_trainer)

# Create a new response function
def get_bot_response(user_input):
    # Get the response from the chatbot
    bot_response = Cogi.get_response(user_input)

    # If the response is empty, return a default response
    if bot_response == '':
        return "I'm sorry, I don't understand."

    # Return the response
    return bot_response

# Define a route for the chatbot response
@app.route('/get')
def get_bot_response():
    user_input = request.args.get('msg')
    bot_response = get_bot_response(user_input)
    return bot_response