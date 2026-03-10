import torch
import torch.nn as nn


class BiLSTMCRF(nn.Module):

    def __init__(self, vocab_size, embedding_dim, hidden_dim, tagset_size):
        super(BiLSTMCRF, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim // 2,
            num_layers=1,
            bidirectional=True,
            batch_first=True
        )

        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):

        embeddings = self.embedding(sentence)

        lstm_out, _ = self.lstm(embeddings)

        emissions = self.hidden2tag(lstm_out)

        return emissions
