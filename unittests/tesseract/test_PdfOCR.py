import unittest
import os
import sys
import pickle
import pytesseract
import pandas as pd

root_dir = "/home/ubuntu" if sys.platform == "linux" else "E:\\GitHub"
sys.path.append(root_dir)

import PdfVectorStore.cons as cons
from PdfVectorStore.encoders.bgeEncoder import BgeEncoder
from PdfVectorStore.tesseract.pdfOCR import pdfOCR

pdfFpath = os.path.join(root_dir, 'PdfVectorStore', 'unittests','data','0.pdf')
exp_aggDict_fpath = os.path.join(root_dir, 'PdfVectorStore', 'unittests','data','exp_aggDict.pickle')
encoder = BgeEncoder()

if sys.platform != "linux":
    pytesseract.pytesseract.tesseract_cmd = cons.tesseract_exe_fpath

if False:
    with open(exp_aggDict_fpath, 'wb') as f:
        pickle.dump(pdfOCR(pdfFpath, encoder, dpi=cons.dpi, poppler_path=cons.poppler_path), f)
else:
    with open(exp_aggDict_fpath, 'rb') as f:
        exp_aggDict = pickle.load(f)

class Test_PdfOCR(unittest.TestCase):
    """"""

    def setUp(self):
        self.encoder = encoder
        self.obs_aggDict = pdfOCR(pdfFpath, encoder, dpi=cons.dpi, poppler_path=cons.poppler_path)
        self.exp_aggDict = exp_aggDict
        self.obs_aggDf = pd.DataFrame.from_records(self.obs_aggDict)
        self.exp_aggDf = pd.DataFrame.from_records(self.exp_aggDict)

    def test_type(self):
        self.assertEqual(type(self.obs_aggDict),type(self.exp_aggDict))
    def test_len(self):
        self.assertEqual(len(self.obs_aggDict),len(self.exp_aggDict))
    def test_shape(self):
        self.assertEqual(self.obs_aggDf.shape,self.exp_aggDf.shape)
    def test_columns(self):
        self.assertEqual(self.obs_aggDf.columns.to_list(),self.exp_aggDf.columns.to_list())

if __name__ == "__main__":
    unittest.main()
