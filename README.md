# FastAPI Patient Management Service

A modern, cloud-ready microservice built with FastAPI.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Running the Service](#running-the-service)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [CI/CD](#cicd)
- [License](#license)

## 🏗️ Architecture

```
fastapi-service/
├── src/                      # Application source code
│   ├── api/                  # API layer (routes, handlers, exceptions)
│   ├── core/                 # Core functionality and configuration
│   ├── models/               # Pydantic data models
│   ├── storage/              # Data persistence layer
│   └── main.py               # Application entry point
├── tests/                    # Test suite
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
└── pyproject.toml           # Project configuration
```

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints

## 🚀 Quick Start

**Recommended: Docker** (fastest way to get started)

```bash
git clone https://github.com/deanna-spinks/fastapi-service.git
cd fastapi-service
docker build -t fastapi-service .
docker run -p 8000:8000 --env-file .env.development fastapi-service
```

Visit http://localhost:8000/docs for interactive API documentation.

## 🏃 Running the Service

### Option 1: Docker (Recommended)

**Development:**
```bash
docker build -t fastapi-service .
docker run -p 8000:8000 --env-file .env.development fastapi-service
```

**Production:**
```bash
docker build -f Dockerfile.prod -t fastapi-service:prod .
docker run -p 8000:8000 --env-file .env.prod fastapi-service:prod
```

Configure via `PORT` and `LOG_LEVEL` environment variables.

### Option 2: Local Development

**Prerequisites:** Python 3.13+

1. **Clone and setup**
   ```bash
   git clone https://github.com/deanna-spinks/fastapi-service.git
   cd fastapi-service
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the service**
   ```bash
   uvicorn src.main:app --reload
   ```

The service will be available at http://localhost:8000

## 📚 API Documentation

Once the service is running, visit:

- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Available Endpoints

#### Health Check
```
GET /health
```
Returns service health status

#### Root
```
GET /
```
Returns "FastAPI Service is running" message

#### Patient Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients/` | List all patients |
| POST | `/patients/` | Create a new patient |
| GET | `/patients/{id}` | Get a specific patient |
| PATCH | `/patients/{id}` | Partially update a patient |
| DELETE | `/patients/{id}` | Delete a patient |

#### Example: Create a Patient

```bash
curl -X POST "http://localhost:8000/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 35,
    "gender": "male",
    "email": "john.doe@example.com",
    "phone": "03 9876 5432"
  }'
```

## Testing

```bash
# Quick way (using Makefile)
make test              # Run all tests with coverage (currently: unit tests only)
make test-unit         # Run unit tests only
make lint              # Check code quality
make ci                # Simulate full CI/CD pipeline locally

# Or directly with pytest
pytest                 # Run all tests (currently: unit tests only)
pytest --cov=src       # Run with coverage report
pytest tests/unit-tests/ -v  # Run unit test suite
```

### Test Structure
- ✅ **Unit Tests** (`tests/unit-tests/`) - Fast, isolated component tests (implemented)
- 🚧 **Integration Tests** (`tests/integration/`) - API endpoint testing (planned)
- 🚧 **E2E Tests** (`tests/e2e/`) - Full user journey testing (planned)
- 📋 **Performance Tests** (`tests/performance/`) - Load and stress testing (future)

Coverage threshold: **80%** (enforced by CI/CD on implemented tests)

## 🚀 CI/CD

This project includes **production-ready CI/CD pipelines** for GitHub Actions.

### GitHub Actions
- ✅ **Automated testing** on pull requests (~9 minutes)
- ✅ **Code quality checks** (linting, formatting, type checking)
- ✅ **Security scanning** (Trivy, dependency checks)
- ✅ **Docker image builds** and publishing to GitHub Container Registry
- ✅ **Path filtering** - Only runs on code changes (skips documentation-only commits)
- ✅ **Coverage reporting** with Codecov integration

**Pipeline Behavior:**
- 🔹 **Feature branches:** Pipeline runs when you open/update a PR (not on push)
- 🔹 **Main/Develop:** Pipeline runs on every push (~10-12 minutes)
- 🔹 **Publish:** Docker images published automatically on merge to main

### Quick Commands

```bash
# Simulate CI/CD locally before pushing
make ci

# Quick pre-commit check
make pre-commit

# Run what the pipeline runs
make lint && make test && make docker-build
```

## 📄 License

See [LICENSE](LICENSE)

## 📧 Contact

For questions or support, contact: admin@deannaspinks.onmicrosoft.com
