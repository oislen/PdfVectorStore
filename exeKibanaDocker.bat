:: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

:: Create a new docker network.
::call docker network create elastic
:: Copy the http_ca.crt SSL certificate from the container to your local machine.
call docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
:: Pull the Kibana Docker image
call docker pull docker.elastic.co/kibana/kibana:8.14.3
:: Start a Kibana container.
call docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.14.3
:: Finished url configuration via es01 token and ver: http://localhost:5601/