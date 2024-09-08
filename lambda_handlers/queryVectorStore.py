import json
import logging

import PdfVectorStore.cons as cons
from PdfVectorStore.elastic.elasticStore import ElasticStore
from PdfVectorStore.encoders.bgeEncoder import BgeEncoder
from PdfVectorStore.utilites.commandlineInterface import commandlineInterface

def lambda_handler(
        text, 
        elastic_index_name, 
        elastic_field, 
        encoder,
        k=10, 
        num_candidates=10
        ):
    """
    """
    
    # set up logging
    lgr = logging.getLogger()
    lgr.setLevel(logging.INFO)
    
    logging.info("Connecting to ElasticStore.")
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
    
    return results

if __name__ == "__main__":
    # set parameters
    text = "Musterkunde"
    elastic_index_name=cons.elastic_index_name
    elastic_field="encoding"
    encoder = BgeEncoder()
    k=10
    num_candidates=10
    operation, pdf_fpath, text = commandlineInterface()
    # call lambda handler
    lambda_handler(
        text=text, 
        elastic_index_name=elastic_index_name, 
        elastic_field=elastic_field,
        encoder=encoder, 
        k=k, 
        num_candidates=num_candidates
        )