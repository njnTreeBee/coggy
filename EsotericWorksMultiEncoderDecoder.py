
import torch
from torch import nn
from torch.nn import Transformer

class EsotericWorksMultiEncoderDecoder(nn.Module):
    def __init__(self, n_enc_dec_pairs, ntoken, ninp, nhead, nhid, nlayers, dropout=0.5):
        super(EsotericWorksMultiEncoderDecoder, self).__init__()

        self.models = nn.ModuleList()
        self.encoders = nn.ModuleList()
        self.decoders = nn.ModuleList()

        for _ in range(n_enc_dec_pairs):
            model = Transformer(ninp, nhead, nhid, nlayers, dropout)
            self.models.append(model)
            self.encoders.append(nn.Embedding(ntoken, ninp))
            self.decoders.append(nn.Linear(ninp, ntoken))

    def forward(self, src, tgt, src_mask=None, tgt_mask=None, memory_mask=None, src_key_padding_mask=None, tgt_key_padding_mask=None, memory_key_padding_mask=None):
        outputs = []

        for model, encoder, decoder in zip(self.models, self.encoders, self.decoders):
            src = encoder(src)
            tgt = encoder(tgt)
            output = model(src, tgt, src_mask, tgt_mask, memory_mask, src_key_padding_mask, tgt_key_padding_mask, memory_key_padding_mask)
            outputs.append(decoder(output))

        return outputs
