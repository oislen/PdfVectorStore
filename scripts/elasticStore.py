import logging
from elasticsearch import Elasticsearch
from copy import copy

pdfMappingDict = {
    "properties" : {
        "invoice_id" : {"type" : "long"},
        "page_num" : {"type" : "long"},
        "block_num" : {"type" : "long"},
        "par_num" : {"type" : "long"},
        "line_num" : {"type" : "long"},
        "left" : {"type" : "long"},
        "top" : {"type" : "long"},
        "width" : {"type" : "long"},
        "height" : {"type" : "long"},
        "text" : {"type" : "keyword"},
        "encoding" : {"type" : "dense_vector", "dims" : 768}
        }
    }

class ElasticStore():
    
    def __init__(self, http_auth, verify_certs=False, elastic_docker_ca_crt_fpath=None, elastic_localhost_url="https://localhost:9200", request_timeout=10):
        self.es = Elasticsearch(
            hosts = [elastic_localhost_url], 
            ca_certs=elastic_docker_ca_crt_fpath, 
            http_auth=http_auth, 
            verify_certs=verify_certs,
            request_timeout=request_timeout
            )
        logging.info(self.es.info())

    def deleteIndex(self, index):
        """
        """
        try:
            #self.es.options().indices.delete(index=index)
            self.es.indices.delete(index=index, ignore=[400, 404])
        except Exception as e:
            logging.error(e)

    def createIndex(self, index, mappings):
        """
        """
        try:
            self.es.indices.create(index=index, mappings=mappings)
        except Exception as e:
            logging.error(e)

    def loadIndex(self, index, documents):
        """
        """
        for i, document in enumerate(documents):
            try:
                document = copy(document)
                id = document['_id']
                del document['_id']
                self.es.index(index=index, id=id, document=document)
            except Exception as e:
                logging.error(i, e)
    
    def listIndices(self, index="*"):
        """
        """
        try:
            elasticIndices = self.es.indices.get_alias(index=index)
        except Exception as e:
            logging.error(e)
            elasticIndices = None
        return elasticIndices

    def getIndexMapping(self, index):
        """
        """
        try:
            elasticIndexMapping = self.es.indices.get_mapping(index=index)
        except Exception as e:
            logging.error(e)
            elasticIndexMapping = None
        return elasticIndexMapping
    
    def getDocumentfromId(self, index, id):
        """
        """
        try:
            document = self.es.get(index=index, id=id)
        except Exception as e:
            logging.error(e)
            document = None
        return document
    
    def vectorSearch(self, text, encoder, elastic_index_name, elastic_field, k=10, num_candidates=10):
        """
        """
        try:
            # encode text for query
            text_encoding = encoder.encode(text=text).tolist()
            # generate elastic query
            elastic_query = {
                "field": elastic_field,
                "query_vector": text_encoding,
                "k": k,
                "num_candidates": num_candidates
                }
            # run the elastic query
            results = self.es.search(index=elastic_index_name, knn=elastic_query)
        except Exception as e:
            logging.error(e)
            results = None
        return results