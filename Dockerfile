# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt 

# Install dependencies
RUN pip install -r requirements.txt 

# Copy the entire social_web directory into the container at /app/social_web/
COPY . .

# Specify the command to run on container start
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
