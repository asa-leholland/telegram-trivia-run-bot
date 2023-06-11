FROM python:3.9-slim

WORKDIR /app

# Copy the bot source code to the container
COPY bot.py /app
COPY init.sql /app

# Install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Create and initialize the database
RUN sqlite3 /app/database.db < /app/init.sql

# Run the bot
CMD ["python", "/app/bot.py"]
