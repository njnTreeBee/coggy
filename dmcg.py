from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chatbot named Cogi
Cogi = ChatBot('Cogi')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(Cogi)

# Train the chatbot on the English corpus
trainer.train('chatterbot.corpus.english')

# Save the trained model to a file
Cogi.trainer.export_for_training('./cogi_training_data.json')