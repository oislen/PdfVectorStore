import sys
import os
import json
import logging
import pytesseract
import pandas as pd

pd.options.display.max_columns = None

sys.path.append(os.getcwd())

import PdfVectorStore.cons as cons
from PdfVectorStore.tesseract.pdfOCR import pdfOCR
from PdfVectorStore.elastic.elasticStore import pdfMappingDict
from PdfVectorStore.elastic.elasticStore import ElasticStore
from PdfVectorStore.elastic.elasticStore import objectToDataFrame
from PdfVectorStore.encoders.bgeEncoder import BgeEncoder
from PdfVectorStore.utilites.commandlineInterface import commandlineInterface

def lambda_handler(
        operation,
        elastic_index_name,
        text=None,
        encoder=None,
        mappings=None,
        pdf_fpath=None,
        elastic_field="encoding",
        k=10,
        num_candidates=10
        ):
    
    """
        Executable lambda handler function for running pdf vector store operations.
        
            Parameters
            ----------
            operation : str
                The operation type to perform; either 'delete_index', 'create_index', 'bulk_index', 'bulk_delete' or 'query_index'.
            elastic_index_name : str
                The name of the elastic index.
            text : str
                The text to search for in the elastic index, default is None.
            encoder : encoder
                The encoder to use for encoding the text for vector search, default is None.
            mappings : dict
                The mapping structure of the elastic index, default is None.
            pdf_fpath : str
                The .pdf file path to etl into the vector store, default is None.
            elastic_field : str
                The encoding field of the elastic index to vector search, default is 'encoding'.
            k : int
                The number of nearest neighbours to search, default is 10.
            num_candidates : int
                The number of query results to return, default is 10.
            
            Returns
            -------
            results : dict, pandas.DataFrame
                The results of the lambda handler execution
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
        results = es.deleteIndex(index=elastic_index_name)
    # create index
    elif operation == 'create_index':
        logging.info(f"Creating elastic index {elastic_index_name}")
        results = es.createIndex(index=elastic_index_name, mappings=mappings)
    # bulk load data into elastic index
    elif operation == 'bulk_index':
        logging.info(f"Bulk index for elastic index {elastic_index_name}")
        results = es.bulkDocumentIndexDelete(index=elastic_index_name, mappings=mappings, documents=documents, op_type='index')
        logging.info(results)
    # bulk delete data from elastic index
    elif operation == 'bulk_delete':
        logging.info(f"Bulk delete for elastic index {elastic_index_name}")
        results = es.bulkDocumentIndexDelete(index=elastic_index_name, mappings=mappings, documents=documents, op_type='delete')
        logging.info(results)
    # query data from elastic index
    elif operation == 'query_index':
        logging.info("Querying Vector Store.")
        # run the query
        results = es.vectorSearch(
            text=text, 
            encoder=encoder, 
            elastic_index_name=elastic_index_name, 
            elastic_field=elastic_field, 
            k=k, 
            num_candidates=num_candidates
            )
        logging.info(objectToDataFrame(results)[['text','_score']])
    return results

if __name__ == "__main__":
    # python PdfVectorStore\lambda_handlers\pdfVectorStore.py --operation delete_index --elastic_index_name pdfvectorstore
    # python PdfVectorStore\lambda_handlers\pdfVectorStore.py --operation create_index --elastic_index_name pdfvectorstore
    # python PdfVectorStore\lambda_handlers\pdfVectorStore.py --operation bulk_index --pdf_fpath E:\GitHub\PdfVectorStore\data\1.pdf --elastic_index_name pdfvectorstore
    # python PdfVectorStore\lambda_handlers\pdfVectorStore.py --operation bulk_delete --pdf_fpath E:\GitHub\PdfVectorStore\data\1.pdf --elastic_index_name pdfvectorstore
    # python PdfVectorStore\lambda_handlers\pdfVectorStore.py --operation query_index --elastic_index_name pdfvectorstore --text Musterkunde
    # set parameters
    operation, pdf_fpath, elastic_index_name, text = commandlineInterface()
    encoder = None if operation in ["delete_index", "create_index"] else BgeEncoder()
    mappings = None if operation in ["delete_index"] else pdfMappingDict
    # assign tesseract cmd when not linux
    if sys.platform != "linux":
        pytesseract.pytesseract.tesseract_cmd = cons.tesseract_exe_fpath
    # call lambda handler
    lambda_handler(
        operation=operation,
        elastic_index_name=elastic_index_name,
        text=text,
        encoder=encoder,
        mappings=mappings,
        pdf_fpath=pdf_fpath
        )