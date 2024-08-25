import sys
import os
import json
import logging
import pytesseract

sys.path.append(os.path.dirname(os.getcwd()))

from scripts.pdfOCR import pdfOCR
from scripts.elasticStore import ElasticStore
import scripts.cons as cons

# set up logging
lgr = logging.getLogger()
lgr.setLevel(logging.INFO)

# load elastic credientials from .json file
with open(cons.elastic_docker_cred_fpath, "rb") as j:
    elastic_config = json.loads(j.read())

# OCR pdf invoice
pytesseract.pytesseract.tesseract_cmd = cons.tesseract_exe_fpath
documents = pdfOCR(cons.pdf_fpath)

# connect to elastic store
es = ElasticStore(
    http_auth=(elastic_config["user"], elastic_config["password"]), 
    elastic_docker_ca_crt_fpath=cons.elastic_docker_ca_crt_fpath,
    elastic_localhost_url=cons.elastic_localhost_url, 
    request_timeout=10
    )

# load data into elastic index
es.loadIndex(index=cons.elastic_index_name, documents=documents)