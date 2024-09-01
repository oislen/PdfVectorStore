import sys
import os
import json
import logging
import pytesseract

import PdfVectorStore.scripts.cons as cons
from PdfVectorStore.scripts.pdfOCR import pdfOCR
from PdfVectorStore.scripts.elasticStore import ElasticStore

# set up logging
lgr = logging.getLogger()
lgr.setLevel(logging.INFO)

# load elastic credientials from .json file
with open(cons.elastic_docker_cred_fpath, "rb") as j:
    elastic_config = json.loads(j.read())

# OCR pdf invoice
documents = pdfOCR(pdfFpath=cons.pdf_fpath, dpi=cons.dpi, poppler_path=cons.poppler_path)

# connect to elastic store
es = ElasticStore(
    http_auth=(elastic_config["user"], elastic_config["password"]), 
    elastic_docker_ca_crt_fpath=cons.elastic_docker_ca_crt_fpath,
    elastic_localhost_url="https://host.docker.internal:9200", 
    request_timeout=cons.elastic_request_timeout
    )

# load data into elastic index
es.loadIndex(index=cons.elastic_index_name, documents=documents)