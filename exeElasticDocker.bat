:: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

:: Create a new docker network.
call docker network create elastic
:: Pull the Elasticsearch Docker image.
call docker pull docker.elastic.co/elasticsearch/elasticsearch:8.14.3
:: Start an Elasticsearch container.
call docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.14.3
:: Copy the http_ca.crt SSL certificate from the container to your local machine.
call docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .

:: Pull the Kibana Docker image
call docker pull docker.elastic.co/kibana/kibana:8.14.3
:: Start a Kibana container.
call docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.14.3