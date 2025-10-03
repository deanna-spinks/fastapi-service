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
   git clone <repository-url>
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

## 📄 License

See [LICENSE](LICENSE)

## 📧 Contact

For questions or support, contact: admin@deannaspinks.onmicrosoft.com
