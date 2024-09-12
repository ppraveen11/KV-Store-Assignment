# Use the official Python image
FROM python:3.9-slim
WORKDIR /app
COPY key-vault.py /app
RUN pip install prometheus_client

# 8000 for Prometheus metrics
EXPOSE 8000
# Expose Fot service port 8080
EXPOSE 8080

CMD ["python", "key-vault.py"]

