
import torch
import torch.nn as nn

class GraphNeuralNetwork(nn.Module):
    def __init__(self, num_nodes, num_features, num_classes):
        super(GraphNeuralNetwork, self).__init__()

        self.embedding = nn.Embedding(num_nodes, num_features)
        self.conv1 = nn.Conv1d(num_features, 16, 3)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(16, 32, 3)
        self.fc1 = nn.Linear(32 * (num_nodes - 2), 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x, edge_index):
        x = self.embedding(x)
        x = self.conv1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = x.view(-1, x.size(1))
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
