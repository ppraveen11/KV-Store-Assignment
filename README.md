This repository contains a simple key-value store implemented in Python. The service provides endpoints to set, get, and search for keys. Prometheus metrics are exposed to monitor request latency, HTTP status codes, and the total number of keys in the store.

## Getting Started

### Prerequisites

- Docker
- Kubernetes (for deployment)

### Build the Docker image:

```bash
docker build -t kv-store .
```

### After building the image, run the container with the following command:
```bash

docker run -p 8080:8080 -p 8000:8000 kv-store-prometheus
```

Port 8080 will be used for your key-value store API.
Port 8000 will be used for Prometheus metrics

### Verify the APIs

#### Set a key:

 ```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "abc-1", "value": "123"}' http://localhost:8080/set
 ```
#### Get a key:

```bash
curl http://localhost:8080/get/abc-1
```
### To access the Prometheus metrics

```bash
curl http://localhost:8000/metrics
```
You should see Prometheus metrics like request latency, status codes, and the total number of keys in the response.

![image](https://github.com/user-attachments/assets/e6b22707-5a28-4766-b6a4-13aaf649db55)

# Deployement on kubernetes
Before make ensure the the image has pushed to the docker hub repository before going deploy on kubernetes

```bash
kubectl apply -f  deployment.yaml
kubectl apply -f  service.yaml
Kubectl apply -f  ingress.yaml
```
#### Use Port Forwarding for Testing
```bash
kubectl port-forward service/kv-store 8080:80  8000:8000
```
#### Set a key:
 ```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "abc-1", "value": "123"}' http://localhost:8080/set
 ```
#### Get a key:
```bash
curl http://localhost:8080/get/abc-1
```
### Then access the metrics endpoint:

```bash
curl http://localhost:8000/metrics
```









