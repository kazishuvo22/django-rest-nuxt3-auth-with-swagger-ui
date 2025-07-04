# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for mysqlclient
# These include:
#   - default-libmysqlclient-dev: MySQL client development files (headers, libraries)
#   - gcc: The C compiler
#   - pkg-config: A helper tool for finding libraries
#   - build-essential: (Often includes gcc, g++) sometimes useful, but gcc is explicitly needed here.
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#        default-libmysqlclient-dev \
#        gcc \
#        pkg-config \
#    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000

# Command to run the Django application (as defined in docker-compose.yml)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]