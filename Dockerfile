# get base image
FROM ubuntu:latest

# set environment variables
ENV user=ubuntu
ENV DEBIAN_FRONTEND=noninteractive

# install required software and programmes for development environment
RUN apt-get update 
RUN apt-get install -y apt-utils vim curl wget unzip git tree htop

# set up home environment
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# install git and pull pdfsearch repo
RUN git clone https://github.com/oislen/PdfVectorStore.git /home/ubuntu/PdfVectorStore

# tesseract dependencies
RUN apt-get install -y libleptonica-dev tesseract-ocr python3-pil tesseract-ocr-eng tesseract-ocr-script-latn

# poppler dependencies
RUN apt-get install -y poppler-utils

# cv2 dependencies
RUN apt-get install -y ffmpeg libsm6 libxext6

# install required python packages
COPY requirements.txt /tmp/
RUN apt-get install -y python3 python3-venv python3-pip
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN /opt/venv/bin/python3 -m pip install -r /tmp/requirements.txt

WORKDIR /home/${user}
CMD ["/opt/venv/bin/python3", "PdfVectorStore/lambda_handlers/pdfVectorStore.py"]