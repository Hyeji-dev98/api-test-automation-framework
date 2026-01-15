# utils/api_client.py
import requests
import time
from config.config import Config

class APIClient:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (GitHub Actions)",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    def get(self, path):
        return self.session.get(self.base_url + path)

    def post(self, path, json=None):
        return self.session.post(self.base_url + path, json=json)

    def put(self, path, json=None):
        return self.session.put(self.base_url + path, json=json)

    def delete(self, path):
        return self.session.delete(self.base_url + path)

    def measure_response_time(self, method, path, json=None):
        start = time.time()
        if method.upper() == 'GET':
            response = self.get(path)
        elif method.upper() == 'POST':
            response = self.post(path, json=json)
        elif method.upper() == 'PUT':
            response = self.put(path, json=json)
        elif method.upper() == 'DELETE':
            response = self.delete(path)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        elapsed = time.time() - start
        return response, elapsed

    def close(self):
        self.session.close()
