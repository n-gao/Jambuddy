import torch
import torch.nn as nn

class SuggestionModel(nn.Module):
    def __init__(self, hidden_size):
        super(SuggestionModel, self).__init__()
        self.hidden_size = hidden_size

        self.input = nn.Linear(1, hidden_size)
        self.rnn = nn.LSTM(hidden_size, hidden_size, 2, dropout=0.05)