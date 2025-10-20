import argparse
import asyncio
import httpx
import time
import random

BASE_URL = "http://localhost:8000"
ENDPOINTS = [
    "/",
    "/compute/30",  # Moderate complexity
    "/compute/35",  # High complexity (~500ms+)
]

async def make_request(client, endpoint):
    """Makes a single request and returns the status and latency."""
    try:
        start_time = time.perf_counter()
        response = await client.get(f"{BASE_URL}{endpoint}", timeout=30.0)
        latency = (time.perf_counter() - start_time) * 1000
        return {"endpoint": endpoint, "status": response.status_code, "latency": latency}
    except Exception as e:
        return {"endpoint": endpoint, "status": "ERROR", "latency": 0, "error": str(e)}

async def test_at_rate(rate, duration=60):
    """Tests the service at a specific requests/second rate for a given duration."""
    print(f"Starting test at {rate} req/s for {duration} seconds...")
    
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration:
            request_start = time.time()
            
            # Create a batch of 'rate' number of requests for this second
            tasks = []
            for _ in range(rate):
                endpoint = random.choice(ENDPOINTS)
                tasks.append(make_request(client, endpoint))
            
            # Execute all requests concurrently
            results = await asyncio.gather(*tasks)
            
            # Print a sample of results
            for result in results[:5]:  # Print first 5 to avoid clutter
                print(f"  Endpoint: {result['endpoint']} - Status: {result['status']} - Latency: {result.get('latency', 0):.2f}ms")
            
            request_count += len(results)
            
            # Sleep to maintain the rate
            elapsed = time.time() - request_start
            if elapsed < 1.0:
                await asyncio.sleep(1.0 - elapsed)
    
    print(f"Completed {request_count} requests at ~{rate} req/s")

async def main():
    parser = argparse.ArgumentParser(description="FastAPI APM Load Test Client")
    parser.add_argument("--rates", nargs="+", type=int, default=[10, 100, 500, 1000],
                        help="Request rates to test (requests per second)")
    parser.add_argument("--duration", type=int, default=60,
                        help="Duration for each rate test in seconds")
    
    args = parser.parse_args()
    
    for rate in args.rates:
        await test_at_rate(rate, args.duration)
        print(f"Waiting 10 seconds before next test rate...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
