# PdfVectorStore

## Overview

This repository contains the code for an ETL process which:
1. Extracts text data from .pdf files using Tesseract OCR
2. Encodes the extracted text using HuggingFace encoders
3. Loads the encoded text data into ElasticSearch
4. Searches ElasticSearch for text queries

## Execution

The repository has been containerised for all ETL and query operations.

### Vector Search

    docker run --name pdf01 --net elastic --publish 8501:8501 --volume E:\GitHub\PdfVectorStore\.cred:/home/ubuntu/PdfVectorStore/.cred --rm oislen/pdfvectorstore:latest  --operation query_index --elastic_index_name pdfvectorstore --text Musterkunde