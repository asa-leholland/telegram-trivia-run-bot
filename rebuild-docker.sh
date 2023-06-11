#!/bin/bash

ENV_FILE_PATH=".env"  # Specify the directory path where the .env file should be located

if [ ! -f "$ENV_FILE_PATH" ]; then
  echo "ERROR: .env file not found in $ENV_FILE_PATH!"
  exit 1
fi

critical_variables=("QUEST_TRACKER_BOT_TOKEN")  # Add other critical variables here if needed

if [ ! -f "$ENV_FILE_PATH" ]; then
  echo "ERROR: .env file not found in $ENV_FILE_PATH!"
  exit 1
fi

for variable in "${critical_variables[@]}"; do
  if grep -qE "^\s*[^#]*$variable=" "$ENV_FILE_PATH"; then
    value=$(grep -E "^\s*[^#]*$variable=" "$ENV_FILE_PATH" | cut -d '=' -f 2- | grep -vE '^\s*#')

    if [ -z "$value" ] || [ "$value" == "''" ] || [ "$value" == '""' ]; then
      if grep -qE "^\s*#[^#]*$variable=" "$ENV_FILE_PATH"; then
        echo "ERROR: '$variable' property in .env file is commented out!"
      else
        echo "ERROR: '$variable' property in .env file is either empty or set to an empty string!"
      fi
      exit 1
    fi
  else
    if grep -qE "^\s*#[^#]*$variable=" "$ENV_FILE_PATH"; then
      echo "ERROR: '$variable' property in .env file is commented out!"
    else
      echo "ERROR: .env file in $ENV_FILE_PATH does not contain '$variable' property!"
    fi
    exit 1
  fi
done


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
