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
        "text" : {"type" : "keyword"}
        }
    }

class ElasticStore():
    
    def __init__(self, http_auth, elastic_docker_ca_crt_fpath, elastic_localhost_url="https://localhost:9200", request_timeout=10):
        self.es = Elasticsearch(
            hosts = [elastic_localhost_url], 
            ca_certs=elastic_docker_ca_crt_fpath, 
            http_auth=http_auth, 
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
            elasticIndices = self.es.indices.get_alias(index)
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