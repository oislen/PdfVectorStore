import unittest
import os
import sys
import pickle

sys.path.append(os.getcwd())

from encoders.bgeEncoder import BgeEncoder

encoder = BgeEncoder()
text = "This is a test sentence for encoding."
exp_encoding_fpath = os.path.join(os.getcwd(), 'unittests','data','exp_encoding.pickle')

if False:
    with open(exp_encoding_fpath, 'wb') as f:
        pickle.dump(encoder.encode(text = text), f)
else:
    with open(exp_encoding_fpath, 'rb') as f:
        exp_encoding = pickle.load(f)

class Test_BgeEncoder(unittest.TestCase):
    """"""

    def setUp(self):
        self.encoder = encoder
        self.text = text
        self.obs_encoding = encoder.encode(text = text)
        self.exp_encoding = exp_encoding

    def test_type(self):
        self.assertEqual(type(self.obs_encoding),type(self.exp_encoding))
    def test_shape(self):
        self.assertEqual(self.obs_encoding.shape,self.exp_encoding.shape)
    def test_object(self):
        self.assertEqual(list(self.obs_encoding),list(self.exp_encoding))

if __name__ == "__main__":
    unittest.main()
