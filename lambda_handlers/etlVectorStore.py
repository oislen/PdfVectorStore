import sys
import json
import logging
import pytesseract

import PdfVectorStore.scripts.cons as cons
from PdfVectorStore.scripts.pdfOCR import pdfOCR
from PdfVectorStore.scripts.elasticStore import pdfMappingDict
from PdfVectorStore.scripts.elasticStore import ElasticStore
from PdfVectorStore.scripts.bgeEncoder import BgeEncoder

def lambda_handler(
        operation,
        elastic_index_name,
        encoder=None,
        mappings=None,
        pdf_fpath=None
        ):
    
    """
    """
    
    # set up logging
    lgr = logging.getLogger()
    lgr.setLevel(logging.INFO)
    
    # if pdf file path is given
    if (pdf_fpath != None) and (encoder != None) and operation in ("bulk_index","bulk_delete"):
        logging.info(f"OCR-ing .pdf file: {cons.pdf_fpath}")
        # OCR pdf invoice
        documents = pdfOCR(pdfFpath=pdf_fpath, dpi=cons.dpi, poppler_path=cons.poppler_path, encoder=encoder)
    
    logging.info("Connecting to ElasticStore")
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
    
     # delete index
    if operation == 'delete_index':
        logging.info(f"Deleting elastic index {elastic_index_name}")
        es.deleteIndex(index=elastic_index_name)
    # create index
    elif operation == 'create_index':
        logging.info(f"Creating elastic index {elastic_index_name}")
        es.createIndex(index=elastic_index_name, mappings=mappings)
    # bulk load data into elastic index
    elif operation == 'bulk_index':
        logging.info(f"Bulk index for elastic index {elastic_index_name}")
        es.bulkDocumentIndexDelete(index=elastic_index_name, mappings=mappings, documents=documents, op_type='index')
    # bulk delete data from elastic index
    elif operation == 'bulk_delete':
        logging.info(f"Bulk delete for elastic index {elastic_index_name}")
        es.bulkDocumentIndexDelete(index=elastic_index_name, mappings=mappings, documents=documents, op_type='delete')

if __name__ == "__main__":
    # set parameters
    operation="bulk_index"
    elastic_index_name=cons.elastic_index_name
    encoder = BgeEncoder()
    mappings=pdfMappingDict
    pdf_fpath=cons.pdf_fpath
    # assign tesseract cmd when not linux
    if sys.platform != "linux":
        pytesseract.pytesseract.tesseract_cmd = cons.tesseract_exe_fpath
    # call lambda handler
    lambda_handler(
        operation=operation,
        elastic_index_name=elastic_index_name,
        encoder=encoder,
        mappings=mappings,
        pdf_fpath=pdf_fpath
        )