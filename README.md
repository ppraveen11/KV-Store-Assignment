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

### Verify the HTTP API Service

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

![image](https://github.com/user-attachments/assets/de014e08-b1b5-4586-8639-86a07320d19d)


# Deployement on kubernetes
Before proceeding with the deployment, ensure that After the build, the image has been pushed to the Docker Hub repository.

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

### Search for keys with a prefix

```bash
curl "http://localhost:8080/search?prefix=abc"
```

### Search for keys with a suffix:

```bash
curl "http://localhost:8080/search?suffix=-1"
```

### Then access the metrics endpoint:

```bash
curl http://localhost:8000/metrics
```

### To implement observability:

1. Prometheus: Scrape the /metrics endpoint to collect metrics.
2. Grafana: Create dashboards to visualize metrics such as request latency, HTTP status codes, and key counts.
3. Alerting: Set up alerts in Prometheus for high latency or error rates.

### Testing
Before releasing to production, perform the following tests:

1. Unit Tests: Ensure that individual components work as expected.
2. Integration Tests: Verify the integration of different parts of the system.
3. Load Testing: Test how the system performs under load.
4. End-to-End Testing: Validate the entire workflow from setting keys to querying metrics.
5. Security Testing: Check for vulnerabilities and ensure secure access to the service.












