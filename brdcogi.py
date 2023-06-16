import chatterbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request

# Initialize the chatbot
cogi = chatterbot.ChatBot('Cogi')

# Train the chatbot on a dataset of conversations
trainer = chatterbot.trainers.ChatterBotCorpusTrainer(cogi)
trainer.train("chatterbot.corpus.english")

# Create a Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the chatbot response
@app.route('/get')
def get_bot_response():
    user_input = request.args.get('msg')
    bot_response = str(cogi.get_response(user_input))
    return bot_response

# Define a route for training the chatbot
@app.route('/train')
def train_bot():
    trainer.train("path/to/custom/conversations")
    return "Training successful!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)