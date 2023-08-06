import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader
import torch.nn.functional as F
from tqdm import tqdm
from cnn import CharCNN
from tokenizer import ByteCharEncoder
from functools import partial

class CharEmbedder(nn.Module):
    
    def __init__(self, hidden_size, max_length=15, kernels=[2, 3, 4]):
        
        super().__init__()
        
        self.hidden_size = hidden_size
        self.char_transformer = ByteCharEncoder()
        self.embedding = nn.Embedding(256 + 1, hidden_size, padding_idx=0)
        self.cnn = CharCNN(hidden_size, kernels=kernels)
                
        self.max_length = max_length
        
    def forward(self, indexes):
        
        x = self.embedding(indexes) # [B, W, C, H]
        B, W, C, H = x.size()
        x = x.view(B * W, C, H) # [B * W, C, H]
        x = self.cnn(x) # [B * W, H]
        x = x.view(B, W, H)
                
        return F.normalize(x, dim=2)
        
    def direct_forward(self, list_tokens):
        indexes = self.char_transformer.encode_batch_with_length(list_tokens, length=self.max_length) # [B, W, C]
        return self.forward(indexes)
    
    def create_dataloader(self, list_tokens, **kwargs):
        return DataLoader(list_tokens, collate_fn=partial(self.char_transformer.encode_batch_with_length, length=self.max_length), **kwargs)
    
    @torch.no_grad()
    def compute_embeddings(self, list_tokens, pbar=True, device='cpu', **kwargs):
        
        self.to(device)
        
        loader = self.create_dataloader(list_tokens, **kwargs)
        
        embeddings = []
        
        if pbar:
            loader = tqdm(loader, desc='compute embeddings')
        
        for x in loader:
            
            x = x.to(device)
            
            e = self.forward(x)
            
            embeddings.append(e.cpu())
            
        return pad_sequence([i for k in embeddings for i in k], batch_first=True)