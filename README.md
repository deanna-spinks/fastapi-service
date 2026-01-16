# FastAPI Patient Management Service

⚠️ Status: WIP / Exploratory / Learning Project  

A small, realistic backend service demonstrating API design, data handling, and cloud deployment, built with FastAPI. 

It is designed for demonstration and collaboration purposes only — no real patient data is included.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Running the Service](#running-the-service)
- [API Documentation](#api-documentation)
- [Testing](#testing)
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
- **[Docker](https://docs.docker.com)** - Containerised for distribution and testing

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
# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

## 📄 License

See [LICENSE](LICENSE)

## 📧 Contact

For questions or support, contact: admin@deannaspinks.onmicrosoft.com
