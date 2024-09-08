import os
import sys

# directory settings
root_dir = "/home/ubuntu/PdfVectorStore" if sys.platform == "linux" else "E:\\GitHub\\PdfVectorStore"
cred_dir = os.path.join(root_dir, ".cred")
data_dir = os.path.join(root_dir, "data")
pdf_fpath = os.path.join(data_dir, "1.pdf")

# poppler and tesseract settings
poppler_path = None if sys.platform == "linux" else 'C:\\poppler-23.11.0\\Library\\bin'
tesseract_exe_fpath = None if sys.platform == "linux" else 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
dpi = 500

# elastic and kibana settings
elastic_localhost_url = "https://host.docker.internal:9200" if sys.platform == "linux" else "https://localhost:9200"
elastic_docker_ca_crt_fpath = os.path.join(cred_dir, "http_ca.crt")
elastic_docker_cred_fpath = os.path.join(cred_dir, "elastic.json")
elastic_index_name = "pdfvectorstore"
elastic_request_timeout = 10
browser_kibana_url = "http://localhost:5601/app/home#/"
browser_elastic_url = "https://localhost:9200"