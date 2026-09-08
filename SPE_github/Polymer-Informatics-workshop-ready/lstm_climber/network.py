import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical

class LanguageModel(pl.LightningModule):
    def __init__(self, hidden_dim, n_layers, len_alphabet, len_molecule, lr = 1e-3,
            dropout = 0.2, verbose = True):
        super().__init__()
        self.save_hyperparameters()
        self.hidden_dim = hidden_dim
        self.len_alphabet = len_alphabet
        self.len_molecule = len_molecule
        self.dropout = dropout
        self.verbose = verbose
        self.learning_rate = lr

        self.lstm = nn.LSTM(
            self.len_alphabet, 
            hidden_dim,
            num_layers = n_layers,
            dropout = dropout,
            batch_first = True
        )
        self.linear = nn.Linear(hidden_dim, self.len_alphabet)

        self.loss_fn = nn.CrossEntropyLoss()    # assume logit input
    def forward(self, x, hidden = None):
        # x = [batch_size, len_molecule, len_alphabet]
        out, hidden = self.lstm(x, hidden)
        out = self.linear(out)
        return out, hidden

    def training_step(self, batch, batch_idx):
        x, y = batch
        x = x.type(torch.FloatTensor).to(self.device)
        y = y.to(self.device)
        
        pred, hidden = self(x)
        pred = pred.view(-1, self.len_alphabet)     # [batch_size * len_molecule, len_alphabet]
        labels = y.argmax(dim=-1).view(-1)          # [batch_size * len_alphbaet * len_molecule]

        loss = self.loss_fn(pred, labels)
        accuracy = (pred.argmax(dim=-1) == labels).float().mean()

        self.log('train_accuracy', accuracy, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        x = x.type(torch.FloatTensor).to(self.device)
        y = y.to(self.device)

        pred, hidden = self(x)
        pred = pred.view(-1, self.len_alphabet)     # [batch_size * len_molecule, len_alphabet]
        labels = y.argmax(dim=-1).view(-1)          # [batch_size * len_alphabet * len_molecule]

        # metrics
        loss = self.loss_fn(pred, labels)
        accuracy = (pred.argmax(dim=-1) == labels).float().mean()
        
        self.log('val_accuracy', accuracy, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    def sample(self, starting_seq, num_samples, temperature = 1.0):
        ''' Sample the model using some starting_seed (one-hot encoded)
        starting seed : [num_starting_chars, len_alphabet]
        Can be a single starting character [1, len_alphabet]
        '''
        self.eval()
        
        with torch.no_grad():
            starting_seq = starting_seq.type(torch.FloatTensor)
            while len(starting_seq.shape) <= 2:
                starting_seq = starting_seq.unsqueeze(0)

            len_seq = starting_seq.size(1)
            hidden = None
            
            # batch sampling (tile the input)
            starting_seq = torch.tile(starting_seq, (num_samples, 1, 1))
            output = [starting_seq]

            # seeding stage
            samp_steps = self.len_molecule - len_seq
            # for i in range(num_samples):
            for _ in range(samp_steps):
                starting_seq = starting_seq.to(self.device)
                out, hidden = self.forward(starting_seq, hidden)
                out = out/temperature
                out = out[:, -1, :].unsqueeze(1)     # selecting final character

                out = out.softmax(dim=-1)
                # dist = Categorical(out.squeeze())
                dist = Categorical(out)
                next_char = F.one_hot(dist.sample(), self.len_alphabet).type(torch.FloatTensor)
                # while len(next_char.shape) <= 2:
                #     next_char = next_char.unsqueeze(0)
                output.append(next_char)

                starting_seq = next_char

        return torch.cat(output, dim=1)


    
