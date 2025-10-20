# FastAPI APM | Production-Ready Monitoring Stack with Grafana-Prometheus
(https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/username/project-name/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/username/project-name/actions/workflows/ci-cd.yml)
[![Code Coverage](https://codecov.io/gh/username/project-name/branch/main/graph/badge.svg)](https://codecov.io/gh/username/project-name)

A brief description of your project.

## Features

- Feature 1
- Feature 2
- Feature 3

# Project Name

> **Minimal, production-ready template for [FastAPI | AI/ML] projects**  
> Batteries included: Docker, testing, linting, and CI-ready structure.

## ✨ Features
- **Zero-config setup**: `make install` → ready to code
- **Dockerized**: One-command container build
- **Testing**: Pre-configured pytest
- **Linting**: Ruff (blazing fast) + Black compatibility
- **Structured**: Follows [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

# 📊 Architecture
``bash
FastAPI App → Prometheus Metrics → Grafana Dashboards
     ↑
  Load Test Client
``

## 🚀 Quick Start
### Prerequisites
- Python 3.12 or higher
- Podman or Docker with Docker Compose
- UV (recommended) or pip

```bash
# Clone and enter the project
git clone  https://github.com/pydev369/prometheus-grafana-fastapi
cd fastapi-apm

# Install using UV (recommended)
uv sync --all-extras

# Alternative: Install using pip
pip install -e .[dev,test]

# Start the monitoring stack
podman-compose up -d

# Run the FastAPI application
uvicorn src.fastapi_apm.main:app --reload --host 0.0.0.0 --port 8000

# In a separate terminal, run load tests
test-client --rates 10 100 500 --duration 30
```
## 📦 Dependencies

Managed via pyproject.toml:

Core: Only essential packages
Dev: Testing/linting tools (install with pip install -e .[dev])

## Docker
``bash
docker build -t myapp .
docker run -p 8000:8000 myapp  # FastAPI
# OR
docker run -p 8888:8888 myapp make notebook  # ML

## 📁 Project Structure
``bash
fastapi-apm/
├── src/
│   └── fastapi_apm/
│       ├── __init__.py
│       ├── main.py                 # FastAPI application
│       └── test_client.py          # Load testing client
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboard.yml
│       └── datasources/
│           └── prometheus.yml
├── tests/
│   └── test_client.py
├── scripts/
│   └── deploy.sh
├── prometheus.yml                  # Prometheus configuration
├── podman-compose.yaml             # Container orchestration
├── pyproject.toml                  # Project dependencies & config
├── Dockerfile
└── README.md

``

## 🐳 Running the Stack
``bash
# Start all services
podman-compose up -d

# View logs
podman-compose logs -f

# Stop services
podman-compose down

# Stop and remove volumes
podman-compose down -v
``
