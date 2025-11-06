.PHONY: help install install-dev test test-unit test-integration test-e2e test-all coverage lint format type-check security docker-build docker-run clean

# Default target
help:
	@echo "FastAPI Service - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install all dependencies (including dev tools)"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests with coverage"
	@echo "  make test-unit       Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-e2e        Run end-to-end tests only"
	@echo "  make coverage        Generate HTML coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            Run all linters (ruff, black, isort)"
	@echo "  make format          Auto-format code (black, isort)"
	@echo "  make type-check      Run type checking (mypy)"
	@echo "  make security        Run security scans (safety, bandit)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    Build Docker images"
	@echo "  make docker-run      Run service in Docker"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove generated files"

# Setup
install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install --upgrade pip
	pip install -r requirements-dev.txt

# Testing
test: install-dev
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

test-unit: install-dev
	pytest tests/unit-tests/ -v --cov=src --cov-report=term-missing

test-integration: install-dev
	@if [ -d "tests/integration" ]; then \
		pytest tests/integration/ -v --cov=src --cov-report=term-missing || [ $$? -eq 5 ]; \
	else \
		echo "⚠️  tests/integration/ directory not found - skipping integration tests"; \
	fi

test-e2e: install-dev
	@if [ -d "tests/e2e" ]; then \
		pytest tests/e2e/ -v --cov=src --cov-report=term-missing || [ $$? -eq 5 ]; \
	else \
		echo "⚠️  tests/e2e/ directory not found - skipping E2E tests"; \
	fi

test-all: test-unit test-integration test-e2e
	@echo "All tests completed!"

coverage: test
	@echo "Opening coverage report..."
	open htmlcov/index.html || xdg-open htmlcov/index.html || echo "Open htmlcov/index.html in your browser"

# Code Quality
lint: install-dev
	@echo "Running Ruff..."
	ruff check src/ tests/
	@echo ""
	@echo "Checking code formatting (Black)..."
	black --check src/ tests/
	@echo ""
	@echo "Checking import sorting (isort)..."
	isort --check-only src/ tests/

format: install-dev
	@echo "Formatting with Black..."
	black src/ tests/
	@echo ""
	@echo "Sorting imports with isort..."
	isort src/ tests/
	@echo ""
	@echo "Code formatted!"

type-check: install-dev
	mypy src/ --ignore-missing-imports

security: install-dev
	@echo "Checking dependencies for vulnerabilities..."
	safety check
	@echo ""
	@echo "Scanning code for security issues..."
	bandit -r src/ -f screen

# Docker
docker-build:
	docker build -t fastapi-service:dev -f Dockerfile .
	docker build -t fastapi-service:prod -f Dockerfile.prod .

docker-run:
	docker run -p 8000:8000 --env-file .env.development fastapi-service:dev

# Run development server
dev:
	uvicorn src.main:app --reload --log-level debug

# Run production-like server locally
prod:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf dist/
	rm -rf build/
	@echo "Cleanup complete!"

# CI/CD simulation (run what CI/CD would run)
ci: clean install-dev lint type-check test-all docker-build
	@echo ""
	@echo "✅ All CI/CD checks passed!"
	@echo "Your code is ready to push!"

# Quick check before committing
pre-commit: format lint test-unit
	@echo ""
	@echo "✅ Pre-commit checks passed!"
	@echo "Safe to commit!"
