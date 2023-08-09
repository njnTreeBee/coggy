
import torch
import torch.nn as nn

class TextToTextModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(TextToTextModel, self).__init__()

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size)
        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.linear(x)
        return x
