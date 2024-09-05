import sys
import os
import json
import logging
import pytesseract

import PdfVectorStore.scripts.cons as cons
from PdfVectorStore.scripts.pdfOCR import pdfOCR
from PdfVectorStore.scripts.elasticStore import pdfMappingDict
from PdfVectorStore.scripts.elasticStore import ElasticStore
from PdfVectorStore.scripts.bgeEncoder import BgeEncoder

# set up logging
lgr = logging.getLogger()
lgr.setLevel(logging.INFO)

logging.info(f"OCR-ing .pdf file: {cons.pdf_fpath}")

# initialise encoder
encoder = BgeEncoder()

# OCR pdf invoice
documents = pdfOCR(pdfFpath=cons.pdf_fpath, dpi=cons.dpi, poppler_path=cons.poppler_path, encoder=encoder)

logging.info("Connecting to ElasticStore")

# load elastic credientials from .json file
with open(cons.elastic_docker_cred_fpath, "rb") as j:
    elastic_config = json.loads(j.read())

# connect to elastic store
es = ElasticStore(
    http_auth=(elastic_config["user"], elastic_config["password"]), 
    elastic_docker_ca_crt_fpath=cons.elastic_docker_ca_crt_fpath,
    elastic_localhost_url=cons.elastic_localhost_url, 
    request_timeout=cons.elastic_request_timeout
    )

# list all elastic indices
es.listIndices(index=f"*{cons.elastic_index_name}*")

if False:

    # delete index
    es.deleteIndex(index=cons.elastic_index_name)

    # create index
    es.createIndex(index=cons.elastic_index_name, mappings=pdfMappingDict)

    # get elastic index mapping
    es.getIndexMapping(index=cons.elastic_index_name)

    # bulk load data into elastic index
    es.bulkDocumentIndexDelete(index=cons.elastic_index_name, mappings=pdfMappingDict, documents=documents, op_type='index')

    # bulk delete data from elastic index
    es.bulkDocumentIndexDelete(index=cons.elastic_index_name, mappings=pdfMappingDict, documents=documents, op_type='delete')

    # query document by id
    es.getDocumentfromId(index=cons.elastic_index_name, id='10111')

# run the query
results = es.vectorSearch(text="Musterkunde", encoder=encoder, elastic_index_name=cons.elastic_index_name, elastic_field="encoding", k=10, num_candidates=10)

# print results
results