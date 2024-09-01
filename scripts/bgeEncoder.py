import torch
import transformers

class bgeEncoder(torch.nn.Module):

    """
    https://huggingface.co/BAAI/bge-base-en-v1.5
    """
    
    def __init__(self, model_type='BAAI/bge-base-en-v1.5', max_len=200):
        super(bgeEncoder, self).__init__()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.max_len = max_len
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_type)
        self.model = transformers.AutoModel.from_pretrained(model_type)
        self.model_type = model_type.split('/')[-1]
        
    def encode(self, text, parameters = {}):
        encoded_input = self.tokenizer(text, max_length=self.max_len, padding="max_length", truncation=True, return_tensors='pt')
        _, output = self.model(**encoded_input, return_dict=False)
        encoding = output.cpu().detach().numpy().flatten()
        return encoding
    
    def save(self, model_fpath):
        torch.save(self.state_dict(), model_fpath)

    def load(self, model_fpath):
        self.load_state_dict(torch.load(model_fpath))
        return self
