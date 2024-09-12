from prometheus_client import Counter, Histogram, start_http_server
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

# Metrics
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latency of HTTP requests', ['endpoint'])
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['endpoint', 'status_code'])
TOTAL_KEYS = Counter('total_keys', 'Total number of keys in the store')

# In-memory key-value store
store = {}

class SimpleKVStore(BaseHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        
        # /get/<key> implementation
        if path_parts[1] == 'get':
            key = path_parts[2]
            if key in store:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({key: store[key]}).encode())
                REQUEST_COUNT.labels(endpoint='/get', status_code='200').inc()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Key not found"}).encode())
                REQUEST_COUNT.labels(endpoint='/get', status_code='404').inc()
        
        # /search?prefix=abc or /search?suffix=-1
        elif path_parts[1] == 'search':
            query_params = urllib.parse.parse_qs(parsed_path.query)
            prefix = query_params.get('prefix', [None])[0]
            suffix = query_params.get('suffix', [None])[0]
            result = []

            # Search keys by prefix or suffix
            for key in store:
                if prefix and key.startswith(prefix):
                    result.append(key)
                if suffix and key.endswith(suffix):
                    result.append(key)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            REQUEST_COUNT.labels(endpoint='/search', status_code='200').inc()

        REQUEST_LATENCY.labels(endpoint=self.path).observe(time.time() - start_time)

    def do_POST(self):
        start_time = time.time()
        if self.path == '/set':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            if 'key' in data and 'value' in data:
                store[data['key']] = data['value']
                TOTAL_KEYS.inc()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Key set successfully"}).encode())
                REQUEST_COUNT.labels(endpoint='/set', status_code='200').inc()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid input"}).encode())
                REQUEST_COUNT.labels(endpoint='/set', status_code='400').inc()

        REQUEST_LATENCY.labels(endpoint=self.path).observe(time.time() - start_time)

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleKVStore)
    print('Starting server on port 8080...')
    start_http_server(8000)  # Expose metrics on /metrics
    httpd.serve_forever()

if __name__ == '__main__':
    run()

