import unittest
import os
import sys
import pickle
import json

root_dir = "/home/ubuntu" if sys.platform == "linux" else "E:\\GitHub"
sys.path.append(root_dir)

import PdfVectorStore.cons as cons
from PdfVectorStore.elastic.elasticStore import ElasticStore, pdfMappingDict, objectToDataFrame

# load test documents
test_documents_fpath = os.path.join(root_dir, 'PdfVectorStore', 'unittests','data','test_documents.pickle')
with open(test_documents_fpath, 'rb') as f:
    documents = pickle.load(f)

# load elastic credentials from .json file
with open(cons.elastic_docker_cred_fpath, "rb") as j:
    elastic_config = json.loads(j.read())

# connect to elastic store
es = ElasticStore(
    http_auth=(elastic_config["user"], elastic_config["password"]), 
    elastic_docker_ca_crt_fpath=cons.elastic_docker_ca_crt_fpath,
    elastic_localhost_url=cons.elastic_localhost_url, 
    request_timeout=cons.elastic_request_timeout
    )

# create / delete test elastic indexes
elastic_index_name = "testelasticindex"
obs_create_resultStatus = es.createIndex(index=elastic_index_name, mappings=pdfMappingDict)
obs_bulkindex_results = es.bulkDocumentIndexDelete(index=elastic_index_name, mappings=pdfMappingDict, documents=documents, op_type='index', chunk_size=500)
obs_bulkdelete_results = es.bulkDocumentIndexDelete(index=elastic_index_name, mappings=pdfMappingDict, documents=documents, op_type='delete', chunk_size=500)
obs_delete_resultStatus = es.deleteIndex(index=elastic_index_name)

# load expected outputs
exp_bulkindex_results_fpath = os.path.join(root_dir, 'PdfVectorStore', 'unittests','data','obs_bulkindex_results.pickle')
exp_bulkdelete_results_fpath = os.path.join(root_dir, 'PdfVectorStore', 'unittests','data','obs_bulkdelete_results.pickle')

if False:
    with open(exp_bulkindex_results_fpath, 'wb') as f:
        pickle.dump(obs_bulkindex_results, f)
    with open(exp_bulkdelete_results_fpath, 'wb') as f:
        pickle.dump(obs_bulkdelete_results, f)        
else:
    with open(exp_bulkindex_results_fpath, 'rb') as f:
        exp_bulkindex_results = pickle.load(f)
    with open(exp_bulkdelete_results_fpath, 'rb') as f:
        exp_bulkdelete_results = pickle.load(f)

class Test_ElasticStore(unittest.TestCase):
    """"""

    def setUp(self):
        self.es = es
        self.documents = documents
        self.pdfMappingDict = pdfMappingDict
        self.elastic_index_name = elastic_index_name
        self.obs_create_resultStatus = obs_create_resultStatus
        self.obs_bulkindex_results = obs_bulkindex_results
        self.obs_delete_resultStatus = obs_delete_resultStatus
        self.obs_bulkdelete_results = obs_bulkdelete_results
        self.exp_createdelete_resultStatus = {'status':200}
        self.exp_bulkindex_results = exp_bulkindex_results
        self.exp_bulkdelete_results = exp_bulkdelete_results

    def test_createIndex(self):
        self.assertEqual(type(self.obs_create_resultStatus),type(self.exp_createdelete_resultStatus))
        self.assertEqual(len(self.obs_create_resultStatus), len(self.exp_createdelete_resultStatus))
        self.assertEqual(self.obs_create_resultStatus, self.exp_createdelete_resultStatus)

    def test_bulkIndex(self):
        self.assertEqual(type(self.exp_bulkindex_results),type(self.exp_bulkindex_results))
        self.assertEqual(self.exp_bulkindex_results.shape,exp_bulkindex_results.shape)

    def test_bulkDelete(self):
        self.assertEqual(type(self.exp_bulkdelete_results),type(self.exp_bulkdelete_results))
        self.assertEqual(self.exp_bulkdelete_results.shape,exp_bulkdelete_results.shape)

    def test_deleteIndex(self):
        self.assertEqual(type(self.obs_delete_resultStatus),type(self.exp_createdelete_resultStatus))
        self.assertEqual(len(self.obs_delete_resultStatus), len(self.exp_createdelete_resultStatus))
        self.assertEqual(self.obs_delete_resultStatus, self.exp_createdelete_resultStatus)

if __name__ == "__main__":
    unittest.main()
