:: set docker settings
SET DOCKER_USER=oislen
SET DOCKER_REPO=pdfvectorstore
SET DOCKER_TAG=latest
SET DOCKER_IMAGE=%DOCKER_USER%/%DOCKER_REPO%:%DOCKER_TAG%
SET DOCKER_CONTAINER_NAME=pdf01

:: remove existing docker containers and images
:: docker container prune --force
docker container rm --force %DOCKER_CONTAINER_NAME%
docker rm --force %DOCKER_IMAGE%

:: Create a new docker network.
call docker network create elastic

:: build docker image
call docker build --no-cache --tag %DOCKER_IMAGE% . 

:: run docker container
SET UBUNTU_DIR=/home/ubuntu
call docker run  --name %DOCKER_CONTAINER_NAME% --net elastic --publish 8501:8501 --volume E:\GitHub\PdfVectorStore\.cred:/home/ubuntu/PdfVectorStore/.cred  -it %DOCKER_IMAGE%

:: call docker run --net elastic --publish 8501:8501 --rm %DOCKER_IMAGE%  --operation query_index --elastic_index_name pdfvectorstore --text Musterkunde