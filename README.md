# FastAPI Project with SQL Server

A modern, scalable FastAPI application with SQL Server integration built using clean architecture principles.

## 🚀 Features

- **FastAPI**: Modern, fast web framework for building APIs
- **SQL Server**: Database integration with SQLAlchemy ORM
- **Clean Architecture**: Separation of concerns with layers (API, Services, Repositories)
- **Authentication**: JWT-based authentication system
- **Database Migrations**: Alembic for schema management
- **Environment Configuration**: Pydantic settings management
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Testing**: Comprehensive test suite with pytest
- **Docker**: Containerization support
- **Logging**: Structured logging with structlog
- **Code Quality**: Black, isort, flake8, and mypy integration

## 📁 Project Structure

```
BE/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   ├── database.py         # Database connection
│   │   ├── security.py         # Authentication utilities
│   │   └── logging.py          # Logging configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   └── users.py
│   │   │   └── api.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── auth.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
├── alembic/
│   ├── versions/
│   └── env.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11+
- SQL Server (local or remote)
- Docker (optional)

### 1. Clone and Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

### 3. Database Setup

```bash
# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Docker (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api/test_users.py
```

## 🔧 Development

### Code Formatting

```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Lint with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=FastAPI Project

# Logging
LOG_LEVEL=INFO
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t fastapi-app .

# Run container
docker run -p 8000:8000 fastapi-app
```

### Production Considerations

1. Use environment variables for sensitive data
2. Set up proper logging
3. Configure CORS appropriately
4. Use HTTPS in production
5. Set up monitoring and health checks
6. Configure database connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
