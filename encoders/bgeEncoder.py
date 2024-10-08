import os
import platform

# set huggingface hub directory
if platform.system() == 'Windows':
    huggingface_hub_dir = 'E:\\huggingface\\hub'
    os.environ['HF_HOME'] = huggingface_hub_dir
    os.environ['HF_DATASETS_CACHE'] = huggingface_hub_dir
    os.environ['TORCH_HOME'] = huggingface_hub_dir

import torch
import transformers

class BgeEncoder(torch.nn.Module):

    """
    https://huggingface.co/BAAI/bge-base-en-v1.5
    """
    
    def __init__(self, model_type='BAAI/bge-base-en-v1.5', max_len=200):
        super(BgeEncoder, self).__init__()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.max_len = max_len
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_type)
        self.model = transformers.AutoModel.from_pretrained(model_type)
        self.model_type = model_type.split('/')[-1]
        
    def encode(self, text):
        """
        Encode text using the encoder object.
        
            Parameters
            ----------
            text : str
                The text to encode.
            
            Returns
            -------
            encoding : numpy.array
                The text encoding array.
        """
        encoded_input = self.tokenizer(text, max_length=self.max_len, padding="max_length", truncation=True, return_tensors='pt')
        _, output = self.model(**encoded_input, return_dict=False)
        encoding = output.cpu().detach().numpy().flatten()
        return encoding
    
    def save(self, model_fpath):
        """
        Serialises the encoder model to disk.
        
            Parameters
            ----------
            model_fpath : str
                The file path to serialise the encoder model to disk.
        """
        torch.save(self.state_dict(), model_fpath)

    def load(self, model_fpath):
        """
        Loads the encoder model from disk.
        
            Parameters
            ----------
            model_fpath : str
                The file path to load the encoder model from disk.
            
            Returns
            -------
            self : encoder
                The loaded encoder model.
        """
        self.load_state_dict(torch.load(model_fpath))
        return self
