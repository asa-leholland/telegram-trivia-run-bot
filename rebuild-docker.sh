#!/bin/bash


docker login

# Pull the SQLite image
docker pull keinos/sqlite3:latest

# Build the containers
docker-compose build

# Bring the containers down
docker-compose down

# Start the containers in detached mode
docker-compose up -d

# Get the container name for the web application
container_name=$(docker-compose ps -q bot)

# Open the logs for the web application container
docker logs -f $container_name
