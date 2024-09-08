import argparse

def commandlineInterface():
    
    """
    
    Commandline Interface Documentation
    
    Overview
    
    This allows the programme to be called from the commandline in Linux or the anaconda prompt in Windows.
    
    Parameters
    
    --operation
    --pdf_fpath
    --text
    
    Returns
    
    Commandline inputs specified above 
    
    Example
    
	 # for executing the programme with latest data
	 python exec.py 
    
    """
    
    # define argument parser object
    parser = argparse.ArgumentParser(description = 'Commandline Interface')
    
    # add input arguments
    parser.add_argument("--operation", action = "store", dest = "operation", default = None, type = str, help = "ETL operation.")
    parser.add_argument("--pdf_fpath", action = "store", dest = "pdf_fpath", default = None, type = str, help = "Pdf file path.")
    parser.add_argument("--text", action = "store", dest = "text", default = None, type = str, help = "Query text.")

    # extract input arguments
    args = parser.parse_args()
    operation = args.operation
    pdf_fpath = args.pdf_fpath
    text  = args.text
    
    return operation, pdf_fpath, text