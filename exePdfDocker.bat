:: set docker settings
SET DOCKER_USER=oislen
SET DOCKER_REPO=pdfvectorstore
SET DOCKER_TAG=latest
SET DOCKER_IMAGE=%DOCKER_USER%/%DOCKER_REPO%:%DOCKER_TAG%

:: remove existing docker containers and images
docker container prune -f
docker rm -f %DOCKER_IMAGE%

:: build docker image
call docker build --no-cache -t %DOCKER_IMAGE% . 
::call docker build -t %DOCKER_IMAGE% .

:: run docker container
SET UBUNTU_DIR=/home/ubuntu
call docker run  --name pdf01 --net elastic -p 8501:8501 -it %DOCKER_IMAGE%