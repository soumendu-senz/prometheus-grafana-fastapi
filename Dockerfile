FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Use uv to install from pyproject.toml
COPY pyproject.toml .
RUN uv pip install --system --no-cache-dir .

COPY src/ .

EXPOSE 8031

CMD ["uvicorn", "fastapi_apm.main:app", "--host", "0.0.0.0", "--port", "8031"]