# PdfVectorStore

## Overview
* Configure docker containers with kibana, elasticsearch, and pytesseract
* Design pipeline to extract data from pdf file using pytesseract and store in elastic search as .json object
* Have python scripts for creating / loading elastic search index
* Search extracted pdf data using custom elastic search criteria
* Optional is to create vector store for custom search mechanism
* Use bge encoder to encode line level data from pdf

## Version 1:
* Install kibana and elastic search via docker (https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
* Create qmarkdown poc external to kibana and elastic search containers
* Basic tesseract extraction into .json
* Basic ETL process to load extract pdf data into elastic search
* Use built-in interface and search mechanisms to query data

## Version 2:
* Define custom .json scheme for extracting data from .pdf files
* Create vectorisation mechanism of text data (use bge model from huggingface)
* Expand ETL process to store vectors in elastic search
* Dockerise pdf etl code as a seperate container, independant to kibana and elastic search
* Confugure networks such that all 3 independant docker containers can communicate with each other
* Create custom query method using vectorised data
