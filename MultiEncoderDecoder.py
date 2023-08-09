
import torch
from torch import nn
from torch.nn import Transformer

class MultiEncoderDecoder(nn.Module):
    def __init__(self, n_enc_dec_pairs, ntoken, ninp, nhead, nhid, nlayers, dropout=0.5):
        super(MultiEncoderDecoder, self).__init__()

        self.models = nn.ModuleList()

        for _ in range(n_enc_dec_pairs):
            model = Transformer(ninp, nhead, nhid, nlayers, dropout)
            self.models.append(model)

        self.encoder = nn.Embedding(ntoken, ninp)
        self.decoder = nn.Linear(ninp, ntoken)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None, memory_mask=None, src_key_padding_mask=None, tgt_key_padding_mask=None, memory_key_padding_mask=None):
        outputs = []

        for model in self.models:
            output = model(src, tgt, src_mask, tgt_mask, memory_mask, src_key_padding_mask, tgt_key_padding_mask, memory_key_padding_mask)
            outputs.append(self.decoder(output))

        return outputs
