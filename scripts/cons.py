import os
import sys

root_dir = "/home/ubuntu" if sys.platform == "linux" else "E:\\GitHub\\PdfVectorStore"
cred_dir = os.path.join(root_dir, ".cred")
data_dir = os.path.join(root_dir, "data")
pdf_fpath = os.path.join(data_dir, "1.pdf")
elastic_docker_ca_crt_fpath = os.path.join(cred_dir, "http_ca.crt")
elastic_docker_cred_fpath = os.path.join(cred_dir, "elastic.json")
tesseract_exe_fpath = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
elastic_localhost_url="https://localhost:9200"
elastic_index_name = "pdfvectorstore"