import argparse

def commandlineInterface():
    
    """
    This allows the process to be called from the command line.
    
        Parameters
        ----------
        None
        
        Returns
        -------
        operation : str 
            The operation to perform; one of 'create_index', 'delete_index', 'bulk_index', 'bulk_delete' or 'query_text', default is None
        pdf_fpath : str 
            The full path to the .pdf file to ETL into the specified elastic index, default is None
        elastic_index_name : str 
            The name of the elastic index for the operation to occur against, default is None
        text : str
            The text to search within the elastic index
    """
    
    # define argument parser object
    parser = argparse.ArgumentParser(description = 'Commandline Interface')
    
    # add input arguments
    parser.add_argument("--operation", action = "store", dest = "operation", default = None, type = str, help = "ETL operation.")
    parser.add_argument("--pdf_fpath", action = "store", dest = "pdf_fpath", default = None, type = str, help = "Pdf file path.")
    parser.add_argument("--elastic_index_name", action = "store", dest = "elastic_index_name", default = None, type = str, help = "The target elastic index.")
    parser.add_argument("--text", action = "store", dest = "text", default = None, type = str, help = "Query text.")

    # extract input arguments
    args = parser.parse_args()
    operation = args.operation
    pdf_fpath = args.pdf_fpath
    elastic_index_name = args.elastic_index_name
    text  = args.text
    
    return operation, pdf_fpath, elastic_index_name, text