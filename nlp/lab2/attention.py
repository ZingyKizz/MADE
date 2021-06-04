import torch
import torch.nn as nn
import torch.nn.functional as F
import random


class Encoder(nn.Module):
    def __init__(self, input_dim, emb_dim, enc_hid_dim, dec_hid_dim, dropout, pretrained_embedding=None):
        super().__init__()

        self.input_dim = input_dim
        self.emb_dim = emb_dim
        self.enc_hid_dim = enc_hid_dim
        self.dec_hid_dim = dec_hid_dim
        self.dropout = dropout

        if pretrained_embedding is None:
            self.embedding = nn.Embedding(input_dim, emb_dim)
        else:
            self.embedding = pretrained_embedding

        self.rnn = nn.GRU(emb_dim, enc_hid_dim, bidirectional = True)

        self.fc = nn.Linear(enc_hid_dim * 2, dec_hid_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, src):

        embedded = self.dropout(self.embedding(src))

        outputs, hidden = self.rnn(embedded)

        hidden = torch.tanh(self.fc(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim = 1)))

        return outputs, hidden


class Attention(nn.Module):
    def __init__(self, enc_hid_dim, dec_hid_dim):
        super().__init__()

        self.enc_hid_dim = enc_hid_dim
        self.dec_hid_dim = dec_hid_dim

        self.attn_in = (enc_hid_dim * 2) + dec_hid_dim

        self.attn = nn.Linear(self.attn_in, 1)

    def forward(self, dec_hidden, enc_outputs):

        src_len = enc_outputs.shape[0]

        repeated_dec_hidden = dec_hidden.unsqueeze(1).repeat(1, src_len, 1)

        enc_outputs = enc_outputs.permute(1, 0, 2)

        scores = torch.tanh(self.attn(torch.cat((
            repeated_dec_hidden,
            enc_outputs),
            dim = 2)))

        attention = torch.sum(scores, dim=2)

        return F.softmax(attention, dim=1)


class Decoder(nn.Module):
    def __init__(self, output_dim, emb_dim, enc_hid_dim, dec_hid_dim, dropout, attention, pretrained_embedding=None):
        super().__init__()

        self.emb_dim = emb_dim
        self.enc_hid_dim = enc_hid_dim
        self.dec_hid_dim = dec_hid_dim
        self.output_dim = output_dim
        self.dropout = dropout
        self.attention = attention

        if pretrained_embedding is None:
            self.embedding = nn.Embedding(output_dim, emb_dim)
        else:
            self.embedding = pretrained_embedding

        self.rnn = nn.GRU((enc_hid_dim * 2) + emb_dim, dec_hid_dim)

        self.out = nn.Linear(self.attention.attn_in + emb_dim, output_dim)

        self.dropout = nn.Dropout(dropout)


    def _weighted_encoder_rep(self, dec_hidden, enc_outputs):

        a = self.attention(dec_hidden, enc_outputs)

        a = a.unsqueeze(1)

        enc_outputs = enc_outputs.permute(1, 0, 2)

        weighted_encoder_rep = torch.bmm(a, enc_outputs)

        weighted_encoder_rep = weighted_encoder_rep.permute(1, 0, 2)

        return weighted_encoder_rep


    def forward(self, input, dec_hidden, enc_outputs):

        input = input.unsqueeze(0)

        embedded = self.dropout(self.embedding(input))

        weighted_encoder_rep = self._weighted_encoder_rep(dec_hidden,
                                                          enc_outputs)

        rnn_input = torch.cat((embedded, weighted_encoder_rep), dim = 2)

        output, dec_hidden = self.rnn(rnn_input, dec_hidden.unsqueeze(0))

        embedded = embedded.squeeze(0)
        output = output.squeeze(0)
        weighted_encoder_rep = weighted_encoder_rep.squeeze(0)

        output = self.out(
            torch.cat(
                (output, weighted_encoder_rep, embedded), 
                dim = 1)
            )

        return output, dec_hidden.squeeze(0)


class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, device):
        super().__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.device = device

    def forward(self, src, trg, teacher_forcing_ratio=0.5):

        batch_size = src.shape[1]
        max_len = trg.shape[0]
        trg_vocab_size = self.decoder.output_dim

        outputs = torch.zeros(max_len, batch_size, trg_vocab_size).to(self.device)

        enc_outputs, hidden = self.encoder(src)

        output = trg[0,:]

        for t in range(1, max_len):
            output, hidden = self.decoder(output, hidden, enc_outputs)
            outputs[t] = output
            teacher_force = random.random() < teacher_forcing_ratio
            top1 = output.max(1)[1]
            output = (trg[t] if teacher_force else top1)

        return outputs