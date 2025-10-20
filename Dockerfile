FROM python:3.12-slim

WORKDIR /app

# Install deps
COPY pyproject.toml .
RUN pip install --no-cache-dir "fastapi[standard]" prometheus-fastapi-instrumentor uvicorn

# Copy code
COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
