import os
from pdf2image import convert_from_path
import pytesseract
import pandas as pd

def pdfOCR(pdfFpath, encoder, dpi=500, poppler_path='C:\\poppler-23.11.0\\Library\\bin'):
    """
    Applies OCR to extract data from .pdf files.
    
        Parameters
        ----------
        pdfFpath : str
            The .pdf file path to etl into the vector store.
        encoder : encoder
            The encoder to use for encoding the text for vector search.
        dpi : int
            The dpi for image quality of the OCR.
        poppler_path : str
            The file path to local poppler installation on Windows.
        
        Returns
        -------
        aggDict : list of dicts
            The extracted .pdf data from the OCR process.
    """
    # convert from pdf to images
    docs = convert_from_path(pdf_path=pdfFpath, dpi=dpi, poppler_path=poppler_path)
    # ocr image to data
    dfs = [pd.DataFrame(pytesseract.image_to_data(doc, output_type='dict')).assign(page_num=idx) for idx, doc in enumerate(docs)]
    # concat datafames
    concatDf = pd.concat(objs=dfs, ignore_index=False, axis=0)
    # add invoice_id
    invoice_id = int(os.path.splitext(os.path.basename(pdfFpath))[0])
    concatDf['invoice_id'] = invoice_id
    # aggregate to line level
    filter_missing = concatDf['conf'].astype(float) != -1
    orderyCols = ['invoice_id', 'page_num', 'block_num', 'par_num', 'line_num']
    groupbyCols = ['invoice_id', 'page_num', 'block_num', 'par_num', 'line_num']
    aggDict = {'left':'min', 'top':'min', 'width':'sum', 'height':'max', 'text':' '.join}
    aggDf = concatDf.loc[filter_missing, :].sort_values(by=orderyCols).groupby(by=groupbyCols, as_index=False).agg(aggDict)
    # apply encodering
    aggDf['encoding'] = aggDf['text'].apply(lambda text: encoder.encode(text).tolist())
    # create elastic _id
    idKeys = ["invoice_id", "page_num","block_num","par_num","line_num"]
    aggDf['_id'] = aggDf[idKeys].astype(str).sum(axis=1).astype(int)
    # convert to dict
    aggDict = aggDf.to_dict(orient='records')
    return aggDict

