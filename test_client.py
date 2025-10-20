import requests
import time
import threading
import random

BASE_URL = "http://localhost:8031"
ENDPOINTS = [
    "/",
    "/compute/30",
    "/compute/35"
]

REQUEST_RATES = [10, 100, 500]  # Requests per second

def make_request():
    """Makes a request to a random endpoint."""
    endpoint = random.choice(ENDPOINTS)
    try:
        start = time.time()
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
        latency = (time.time() - start) * 1000
        print(f"Endpoint: {endpoint} - Status: {response.status_code} - Latency: {latency:.2f}ms")
    except Exception as e:
        print(f"Request failed: {e}")

def test_at_rate(rate):
    """Tests the service at a specific request rate for 60 seconds."""
    print(f"Starting test at {rate} req/s for 60 seconds...")
    end_time = time.time() + 60
    while time.time() < end_time:
        start_time = time.time()
        # Launch 'rate' number of requests in this second
        threads = []
        for _ in range(rate):
            t = threading.Thread(target=make_request)
            t.start()
            threads.append(t)
        # Wait for all threads to complete
        for t in threads:
            t.join()
        # Sleep for the remainder of the second
        elapsed = time.time() - start_time
        if elapsed < 1:
            time.sleep(1 - elapsed)

if __name__ == "__main__":
    for rate in REQUEST_RATES:
        test_at_rate(rate)
        time.sleep(10)  # Pause between rate changes
