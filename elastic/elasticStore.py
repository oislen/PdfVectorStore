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
        Deletes a specified elastic index.
        
            Parameters
            ----------
            index : str
                The elastic index name to delete.
            
            Returns
            -------
            resultStatus : dict
                Execution Status; either 200 or 500.
        """
        try:
            self.es.indices.delete(index=index, ignore=[400, 404])
            status = 200
        except Exception as e:
            logging.error(e)
            status = 500
        resultStatus = {'status':status}
        return resultStatus
    
    def createIndex(self, index, mappings):
        """
        Creates a specified elastic index.
        
            Parameters
            ----------
            index : str
                The elastic index name to create.
            mapping : dict
                The elastic index mapping structure.
            
            Returns
            -------
            resultStatus : dict
                Execution Status; either 200 or 500.
        """
        try:
            self.es.indices.create(index=index, mappings=mappings)
            status = 200
        except Exception as e:
            logging.error(e)
            status = 500
        resultStatus = {'status':status}
        return resultStatus
    
    def listIndices(self, index="*"):
        """
        Lists all elastic indexes following the specified pattern.
        
            Parameters
            ----------
            index : str
                The elastic index pattern to list with, default is "*".
            
            Returns
            -------
            elasticIndices : dict
                The listed elastic indexes.
        """
        try:
            elasticIndices = self.es.indices.get_alias(index=index).body
        except Exception as e:
            logging.error(e)
            elasticIndices = {}
        return elasticIndices
    
    def getIndexMapping(self, index):
        """
        Gets the mapping structure of a specified elastic index.
            
            Parameters
            ----------
            index : str
                The name of the elastic index mapping structure to retrieve.
            
            Returns
            -------
            elasticIndexMapping : dict
                The elastic index mapping structure.
        """
        try:
            elasticIndexMapping = self.es.indices.get_mapping(index=index)
        except Exception as e:
            logging.error(e)
            elasticIndexMapping = {}
        return elasticIndexMapping
    
    def getDocumentfromId(self, index, id):
        """
        Retrieves a document from an elastic index using its index id.
        
            Parameters
            ----------
            index : str
                The name of the elastic index to retrieve the document from.
            id : int
                The id of the document to retrieve.
            
            Returns
            -------
            document : dict
                The retrieved elastic index document.
        """
        try:
            document = self.es.get(index=index, id=id)
        except Exception as e:
            logging.error(e)
            document = {}
        return document
    
    def bulkDocumentIndexDelete(self, index, mappings, documents, op_type, chunk_size=500):
        """
        Bulk indexes and deletes documents from a specified elastic index.
        
            Parameters
            ----------
            index : str
                The name of the elastic index to bulk index documents to or delete documents from.
            mappings : dict
                The mapping structure of the elastic index.
            documents : list of dicts
                The documents to bulk index or bulk delete.
            op_type : str
                The operation type to perform; either 'index' or 'delete'.
            chunk_size : int
                The batch size to chunk the documents into, default is 500.
            
            Returns
            -------
            log_results_df : pandas.DataFrame
                The log results of the bulk delete or index operation.
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
            log_results_df = pd.DataFrame()
        return log_results_df
    
    def vectorSearch(self, text, encoder, elastic_index_name, elastic_field, k=10, num_candidates=10):
        """
        Retrieves a document from an elastic index using its index id.
        
            Parameters
            ----------
            text : str
                The text to search for in the elastic index.
            encoder : encoder
                The encoder to use for encoding the text for vector search.
            elastic_index_name : str
                The name of the elastic index to search in.
            elastic_field : str
                The encoding field of the elastic index to vector search.
            k : int
                The number of nearest neighbours to search, default is 10.
            num_candidates : int
                The number of results to return, default is 10.
            
            Returns
            -------
            results : dict
                The search results.
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
            results = self.es.search(index=elastic_index_name, knn=elastic_query).body
        except Exception as e:
            logging.error(e)
            results = {}
        return results

def objectToDataFrame(object_api_response):
    """
    Converts a vector query object api dictionary response to a pandas DataFrame.
    
        Parameters
        ----------
        object_api_response : dict
            The vector query object api dictionary response.
        
        Returns
        -------
        resultsDf : pandas.DataFrame
            The vector query response as a pandas DataFrame.
            
    """
    try:
        # extract out elastic search hits as a dataframe
        hitsDf = pd.DataFrame(object_api_response['hits']['hits'])
        # subset out source as a dataframe
        sourceDf = pd.DataFrame(hitsDf['_source'].to_list())
        # combine hits and source as a resulting dataframe
        resultsDf = hitsDf.join(sourceDf).drop(columns=['_source'])
    except Exception as e:
        logging.error(e)
        resultsDf = pd.DataFrame()
    return resultsDf
