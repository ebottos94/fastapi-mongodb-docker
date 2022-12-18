# fastapi-mongodb-docker
Dockerized Fastapi and MongoDB

# Setup
Create .env file with values like in the .env_template file. 

Example:

MONGO_USERNAME=root

MONGO_PASSWORD=password

# Run project
docker-compose up

# Description
3 container :
* **app** : fastapi application with two endpoint : 
**/api/v1/ingest** and **/api/v1/retrieve**. First endpoint, in post mode, accept two values : key, an integer between 1 and 6, and payload, a string with length between 10 and 255 with random behavior: 90% of responses with code 200 and 10% with code 500, and random response time between 10 and 50 ms. Second endpoint, in get mode, accept as query parameters two datetime values in ISO format, and returns some statistics and some logs in the selected time range. The endpoints are protected by an api key passed via header, the value is set in the file app/security.py. The service is exposed on port 8000, to test it : **http://localhost:8000/docs**
* **locust** : load test based on [Locust](https://locust.io/). The test is implemented in locust/locustfile.py. The service is exposed on port 8089, to run load test : **http://localhost:8089/**
* **mongodb** : a MongoDB container.
