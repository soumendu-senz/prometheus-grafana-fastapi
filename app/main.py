from fastapi import FastAPI
import time

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="fastapi-apm")

# Instrument the app and expose the /metrics endpoint
Instrumentator().instrument(app).expose(app)

def complex_processing(n):
    """Simulates high time/space complexity logic."""
    if n <= 1:
        return n
    return complex_processing(n - 1) + complex_processing(n - 2)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI APM!"}

@app.get("/compute/{n}")
def compute_fibonacci(n: int):
    start_time = time.time()
    result = complex_processing(n)
    processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    return {"result": result, "processing_time_ms": processing_time, "input": n}
