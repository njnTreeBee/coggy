import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import KFold
from torch.optim.lr_scheduler import ReduceLROnPlateau
import json
from models.EsotericWorksMultiEncoderDecoder import EsotericWorksMultiEncoderDecoder
from models.GraphNeuralNetwork import GraphNeuralNetwork
from models.LSTM import LSTM
from models.MultiEncoderDecoder import MultiEncoderDecoder
from models.TextToTextModel import TextToTextModel
from models.TransformerLSTM import TransformerLSTM

# Dataset
class TextDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx]
        y = self.labels[idx]
        return x, y

def load_data(path):
    with open(path, 'r') as file:
        data = json.load(file)
    instructions = [item['instruction'] for item in data]
    outputs = [item['output'] for item in data]
    return instructions, outputs

# Load your data
data, labels = load_data('C:\\Users\\User\\Desktop\\agi\\data\\alpaca_data.json')

# Create your dataset
dataset = TextDataset(data, labels)

# Models to train
models = [LSTM(), MultiEncoderDecoder(), TextToTextModel(), TransformerLSTM(), EsotericWorksMultiEncoderDecoder(), GraphNeuralNetwork()]

# K-Fold Cross validation
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

for fold, (train_ids, val_ids) in enumerate(kfold.split(dataset)):
    print(f'FOLD {fold+1}')
    
    # Dataloaders for this fold
    train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
    val_subsampler = torch.utils.data.SubsetRandomSampler(val_ids)
    
    train_dataloader = DataLoader(dataset, batch_size=32, sampler=train_subsampler)
    val_dataloader = DataLoader(dataset, batch_size=32, sampler=val_subsampler)

    # Iterate over models
    for model in models:
        print(f'Training model: {type(model).__name__}')

        # Criterion
        criterion = nn.MSELoss()
        
        # Optimizer
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        # Scheduler for learning rate
        scheduler = ReduceLROnPlateau(optimizer, 'min')
        
        # Device
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = model.to(device)

        # Training loop
        best_val_loss = float('inf')
        epochs_without_improvement = 0

        for epoch in range(100):
            model.train()
            for i, (x, y) in enumerate(train_dataloader):
                x, y = x.to(device), y.to(device)
                optimizer.zero_grad()
                y_pred = model(x)
                loss = criterion(y_pred, y)
                loss.backward()
                optimizer.step()
            
            # Validate
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for x, y in val_dataloader:
                    x, y = x.to(device), y.to(device)
                    y_pred = model(x)
                    val_loss += criterion(y_pred, y).item()
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                epochs_without_improvement = 0
                torch.save(model.state_dict(), f'C:\\Users\\User\\Desktop\\agi\\models\\best_model_{type(model).__name__}_fold_{fold+1}.pt')
            else:
                epochs_without_improvement += 1
                if epochs_without_improvement == 10:
                    print('Early stopping')
                    break
            
            # Scheduler step
            scheduler.step(val_loss)
            
            print(f'Epoch {epoch+1} Train Loss: {loss.item():.4f} Val Loss: {val_loss:.4f}')
