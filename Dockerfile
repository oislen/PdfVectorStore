# get base image
FROM ubuntu:20.04

# set environment variables
ENV user=ubuntu
ENV DEBIAN_FRONTEND=noninteractive

# install required software and programmes for development environment
RUN apt-get update 
RUN apt-get install -y apt-utils vim curl wget unzip git python3 python3-pip tree htop

# install required python packages
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# set up home environment
RUN useradd ${user}
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# install git and pull pdfsearch repo
RUN git clone https://github.com/oislen/PdfVectorStore.git /home/ubuntu/PdfVectorStore

# tesseract dependencies
RUN apt-get install libleptonica-dev tesseract-ocr python3-pil tesseract-ocr-eng tesseract-ocr-script-latn

# poppler dependencies
RUN apt-get install poppler-utils

# cv2 dependencies
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /home/${user}
CMD ["bash"]