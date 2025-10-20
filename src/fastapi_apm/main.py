from fastapi import FastAPI
from contextlib import asynccontextmanager
import time
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentor
from logger import logger
from fastapi import APIRouter


router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Instrument the application on startup
    Instrumentator().instrument(app).expose(app)
    yield

app = FastAPI(title="fastapi-apm", lifespan=lifespan)


# Auto-instrument HTTP metrics
PrometheusFastApiInstrumentor.instrument_app(app)


def complex_processing(n):
    """Simulates high time/space complexity logic (Fibonacci with large input)."""
    if n <= 1:
        return n
    return complex_processing(n - 1) + complex_processing(n - 2)

@router.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI APM!"}


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/compute/{n}")
def compute_fibonacci(n: int):
    try:
        start_time = time.perf_counter()
        result = complex_processing(n)
        processing_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Computed Fibonacci({n}) = {result} in {processing_time:.3f} ms")
        return {"result": result, "processing_time_ms": processing_time, "input": n}

    except RecursionError:
        logger.error(f"RecursionError: Input {n} is too large for Fibonacci computation.")
        return {"error": "Input too large for Fibonacci computation."}
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": f"An unexpected error {str(e)}."}
    
@app.get("/health")
def health_check():
    return {"status": "healthy"}