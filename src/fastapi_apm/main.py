from fastapi import FastAPI
from contextlib import asynccontextmanager
import time
from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Instrument the application on startup
    Instrumentator().instrument(app).expose(app)
    yield

app = FastAPI(title="fastapi-apm", lifespan=lifespan)

def complex_processing(n):
    """Simulates high time/space complexity logic (Fibonacci with large input)."""
    if n <= 1:
        return n
    return complex_processing(n - 1) + complex_processing(n - 2)

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI APM!"}

@app.get("/compute/{n}")
def compute_fibonacci(n: int):
    start_time = time.perf_counter()
    result = complex_processing(n)
    processing_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
    return {"result": result, "processing_time_ms": processing_time, "input": n}
