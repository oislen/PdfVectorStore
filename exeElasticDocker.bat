:: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

:: Create a new docker network.
::call docker network create elastic
:: Pull the Elasticsearch Docker image.
call docker pull docker.elastic.co/elasticsearch/elasticsearch:8.14.3
:: Start an Elasticsearch container.
call docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.14.3

:: You can regenerate the credentials using the following commands.
:: docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
:: docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana