
import torch
import torch.nn as nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

class TransformerLSTM(nn.Module):
    def __init__(self, input_dim, emb_dim, nhead, nhid, nlayers, output_dim, dropout=0.5):
        super(TransformerLSTM, self).__init__()

        self.input_dim = input_dim
        self.emb_dim = emb_dim
        self.nhead = nhead
        self.nhid = nhid
        self.nlayers = nlayers
        self.output_dim = output_dim

        self.embedding = nn.Embedding(self.input_dim, self.emb_dim)
        self.pos_encoder = PositionalEncoding(self.emb_dim, dropout)

        encoder_layers = TransformerEncoderLayer(self.emb_dim, self.nhead, self.nhid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, self.nlayers)

        self.lstm = nn.LSTM(self.emb_dim, self.nhid, self.nlayers, dropout=dropout)

        self.decoder = nn.Linear(self.nhid, self.output_dim)

        self.init_weights()

    def init_weights(self):
        initrange = 0.1
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, src):
        embedded = self.embedding(src)
        embedded = self.pos_encoder(embedded)
        output = self.transformer_encoder(embedded)
        output, _ = self.lstm(output)
        output = self.decoder(output)
        return output


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return self.dropout(x)
