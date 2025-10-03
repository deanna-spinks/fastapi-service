# FastAPI Patient Management Service

A modern, cloud-ready microservice built with FastAPI.

## 🏗️ Architecture

```
fastapi-service/
└── src/
    └── main.py               # Application entry point
```

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server

## ✅ Prerequisites

- Python 3.13+
- pip for dependency management

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/deanna-spinks/fastapi-service.git
   cd fastapi-service
   ```

2. **Setup virtual environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Service

Ensure the virtual environment is activated then run:
```bash
uvicorn src.main:app --reload
```

The service will be available at `http://localhost:8000`

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

## 📄 License

See [LICENSE](LICENSE)

## 📧 Contact

For questions or support, contact: admin@deannaspinks.onmicrosoft.com
