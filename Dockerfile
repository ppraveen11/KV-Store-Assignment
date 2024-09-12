# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY key-vault.py /app


# Install the required Python packages
RUN pip install prometheus_client


# 8000 for Prometheus metrics
EXPOSE 8000

# Expose port 8080
EXPOSE 8080

# Run the app
CMD ["python", "key-vault.py"]

