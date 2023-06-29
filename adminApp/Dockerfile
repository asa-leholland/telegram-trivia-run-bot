FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /app

# Create the directories for the management command
RUN mkdir -p /app/QuestTrackerAdmin/management/commands

# Copy the management command file into the container
COPY initdb.py /app/QuestTrackerAdmin/management/commands/

# Expose the Django development server port (optional)
EXPOSE 8000

# Run the migrations and table creation command
CMD python manage.py initdb && gunicorn QuestTrackerAdmin.wsgi:application --bind 0.0.0.0:$PORT
