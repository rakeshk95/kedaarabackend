.PHONY: help install install-dev test test-cov lint format clean run run-dev docker-build docker-run docker-compose-up docker-compose-down migrate migrate-create

# Default target
help:
	@echo "Available commands:"
	@echo "  install       - Install production dependencies"
	@echo "  install-dev   - Install development dependencies"
	@echo "  test          - Run tests"
	@echo "  test-cov      - Run tests with coverage"
	@echo "  test-db       - Test database connection"
	@echo "  lint          - Run linting (flake8, mypy)"
	@echo "  format        - Format code (black, isort)"
	@echo "  clean         - Clean up cache files"
	@echo "  run           - Run production server"
	@echo "  run-dev       - Run development server"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker container"
	@echo "  docker-compose-up    - Start services with Docker Compose"
	@echo "  docker-compose-down  - Stop services with Docker Compose"
	@echo "  migrate       - Run database migrations"
	@echo "  migrate-create - Create new migration"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Testing
test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 app/ tests/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

# Running the application
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

run-dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Docker commands
docker-build:
	docker build -t fastapi-app .

docker-run:
	docker run -p 8000:8000 fastapi-app

docker-compose-up:
	docker-compose up --build

docker-compose-down:
	docker-compose down

# Database migrations
migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

# Database connection test
test-db:
	python scripts/test_db_connection.py
