# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy source code
COPY ./fraud /app/fraud
COPY ./setup.py /app/

# Install the package and its dependencies
# The '.' installs the code from setup.py
RUN pip install --no-cache-dir .

# Add any other dependencies here, e.g., from a requirements.txt
# RUN pip install -r requirements.txt