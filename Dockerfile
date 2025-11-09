FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# gcc: Compile C extensions in Python packages (e.g., pydantic-core, uvloop)
# python3-dev: Python header files needed to build C extensions
# curl: Used for Docker healthcheck endpoint testing
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*  # Remove apt cache to reduce image size

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set Python path
ENV PYTHONPATH=/app/src

# Copy source code
COPY src/ ./src/

# Expose port (configurable via PORT env var)
EXPOSE 8000

# Environment variables with defaults
ENV PORT=8000
ENV LOG_LEVEL=debug

# Development: includes --reload flag
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "${PORT}", "--log-level", "${LOG_LEVEL}", "--reload"]
