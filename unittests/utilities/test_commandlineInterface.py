import unittest
import os
import sys
import pickle

root_dir = "/home/ubuntu" if sys.platform == "linux" else "E:\\GitHub"
sys.path.append(root_dir)

from PdfVectorStore.utilities.commandlineInterface import commandlineInterface

obs_operation, obs_pdf_fpath, obs_elastic_index_name, obs_text = commandlineInterface()
exp_operation, exp_pdf_fpath, exp_elastic_index_name, exp_text = None, None, None, None

class Test_commandlineInterface(unittest.TestCase):
    """"""

    def setUp(self):
        self.obs_operation = obs_operation
        self.obs_pdf_fpath = obs_pdf_fpath
        self.obs_elastic_index_name = obs_elastic_index_name
        self.obs_text = obs_text
        self.exp_operation = exp_operation
        self.exp_pdf_fpath = exp_pdf_fpath
        self.exp_elastic_index_name = exp_elastic_index_name
        self.exp_text = exp_text

    def test_operation(self):
        self.assertEqual(self.obs_operation, self.exp_operation)
    def test_pdf_fpath(self):
        self.assertEqual(self.obs_pdf_fpath, self.exp_pdf_fpath)
    def test_elastic_index_name(self):
        self.assertEqual(self.obs_elastic_index_name, self.exp_elastic_index_name)
    def test_text(self):
        self.assertEqual(self.obs_text, self.exp_text)

if __name__ == "__main__":
    unittest.main()
