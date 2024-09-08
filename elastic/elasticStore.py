import logging
import datetime
from copy import copy
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers

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
    
    def bulkDocumentIndexDelete(self, index, mappings, documents, op_type, chunk_size=500):
        """
        """
        try:
            # convert documents to dataframe
            dataframe = pd.DataFrame(documents)
            source_cols = list(mappings["properties"].keys())
            dataframe[['_index', '_op_type']] = (index, op_type)
            dataframe['_source'] = dataframe[source_cols].apply(lambda series: series.to_dict(),axis=1)
            # determine action columns based on operation
            if op_type in ('index'): # create / overwrite operations
                bulk_cols = ['_index', '_op_type', '_id', '_source']
            elif op_type in ('delete'):
                bulk_cols = ['_index', '_op_type', '_id']
            # create elastic actions
            actions = dataframe[bulk_cols].to_dict(orient='records')
            # list of log results to be collected
            log_results = []
            # iterate over streaming bulk generator
            for _, item in helpers.streaming_bulk(client=self.es, actions=actions, index=index, chunk_size=chunk_size):
                # collect log results
                log_result = item[op_type]
                log_result['_op_type'] = op_type
                log_result['timestamp'] = int(datetime.datetime.today().timestamp())
                log_results.append(log_result)
            # convert log results to dataframe
            log_results_df = pd.DataFrame(log_results)
        except Exception as e:
            logging.error(e)
            log_results_df = None
        return log_results_df
    
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

def objectToDataFrame(object_api_response):
    """
    """
    try:
        # extract out elastic search hits as a dataframe
        hitsDf = pd.DataFrame(object_api_response.body['hits']['hits'])
        # subset out source as a dataframe
        sourceDf = pd.DataFrame(hitsDf['_source'].to_list())
        # combine hits and source as a resulting dataframe
        resultsDf = hitsDf.join(sourceDf).drop(columns=['_source'])
    except Exception as e:
        logging.error(e)
        resultsDf = None
    return resultsDf
