import re
import string
import torch
from tqdm import tqdm
from .model import CharEmbedder


def load_index(path):
    return torch.load(path)


class SearchIndex(object):
    
    def __init__(self, text_list, device='cpu', word_tokenizer=None, d_model=100, max_length=15, kernels=[2, 3, 4], **args):
        
        self.text_list = text_list
        
        if word_tokenizer is None:
            word_tokenizer = self.simple_tokenizer
            
        self.word_tokenizer = word_tokenizer
        
        self.model = CharEmbedder(d_model, kernels=kernels, max_length=max_length)
        
        tokenized = []
        for t in tqdm(text_list, desc='tokenization'):
            tokenized.append(self.word_tokenizer(t))
            
        self.embeddings = self.model.compute_embeddings(tokenized, device=device, **args)
        
    def simple_tokenizer(self, txt):
        t = txt.strip().lower()
        t = re.sub(r'([%s])' % re.escape(string.punctuation), r' \1 ', t) 
        t = re.sub(r'\\.', r' ', t) 
        t = re.sub(r'\s+', r' ', t)
        return t.split()
        
    def search(self, query):
        
        query = [self.word_tokenizer(query)]
        query_embedding = self.model.compute_embeddings(query, pbar=False, batch_size=1, device='cpu')
        score = self.embeddings @ query_embedding.transpose(1, 2)
        # max sum
        maxsum = score.max(-2).values.sum(-1)
        
        return torch.argsort(maxsum, dim=0, descending=True).numpy()
    
    def show_topk(self, query, k=10):
        
        res = self.search(query)[:k]
        for r in res:
            print(self.text_list[r])
    
    def save(self, path):
        torch.save(self, path)