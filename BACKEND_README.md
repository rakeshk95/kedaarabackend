# FastAPI Backend Setup Guide

This guide will help you set up and run the FastAPI backend for the Performance Review System.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repository-url>
   cd appfactory-flow
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

1. **Create a `.env` file** in the root directory:
   ```bash
   touch .env
   ```

2. **Add the following environment variables** to `.env`:
   ```env
   # Database Configuration
   DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
   # Example: DATABASE_URL=mssql+pyodbc://sa:password123@localhost/performance_review?driver=ODBC+Driver+17+for+SQL+Server
   
   # Security
   SECRET_KEY=your-super-secret-key-here-change-this-in-production
   
   # JWT Configuration
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   
   # CORS Configuration
   ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000
   ```

## Database Setup

### SQL Server Setup
1. **Install SQL Server** (Express, Developer, or Enterprise edition)
2. **Install SQL Server ODBC Driver**:
   - **Windows**: Download from Microsoft's website
   - **Linux**: Follow Microsoft's installation guide
   - **macOS**: Use Homebrew or download from Microsoft
3. **Create a database**:
   ```sql
   CREATE DATABASE performance_review;
   ```
4. **Create a user** (optional, can use SA):
   ```sql
   CREATE LOGIN appuser WITH PASSWORD = 'your_password';
   USE performance_review;
   CREATE USER appuser FOR LOGIN appuser;
   GRANT CONTROL ON DATABASE::performance_review TO appuser;
   ```
5. **Update the DATABASE_URL** in your `.env` file:
   ```env
   DATABASE_URL=mssql+pyodbc://username:password@server/performance_review?driver=ODBC+Driver+17+for+SQL+Server
   ```

### ODBC Driver Installation
- **Windows**: Download "ODBC Driver 17 for SQL Server" from Microsoft
- **Linux (Ubuntu/Debian)**:
  ```bash
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
  curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
  apt-get update
  ACCEPT_EULA=Y apt-get install -y msodbcsql17
  ```
- **macOS**:
  ```bash
  brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
  brew update
  ACCEPT_EULA=Y brew install msodbcsql17
  ```

## Running the Application

### Development Mode
```bash
python fastapi_implementation.py
```

Or using uvicorn directly:
```bash
uvicorn fastapi_implementation:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn fastapi_implementation:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## Testing the API

### Using Postman
1. Import the `Performance_Review_API.postman_collection.json` file into Postman
2. Set the `base_url` variable to `http://localhost:8000/api/v1`
3. Start testing the endpoints

### Using curl
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Login (replace with actual user data)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@company.com", "password": "password123"}'
```

## Database Migrations (Required for SQL Server)

Since we're using SQL Server, database migrations are required to create the initial schema:

1. **Initialize Alembic**:
   ```bash
   alembic init alembic
   ```

2. **Update alembic.ini** to use your SQL Server connection:
   ```ini
   sqlalchemy.url = mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
   ```

3. **Update env.py** in the alembic directory to import your models:
   ```python
   from fastapi_implementation import Base
   target_metadata = Base.metadata
   ```

4. **Create initial migration**:
   ```bash
   alembic revision --autogenerate -m "Initial schema"
   ```

5. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

6. **For future schema changes**:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   alembic upgrade head
   ```

## Project Structure

```
appfactory-flow/
├── fastapi_implementation.py    # Main FastAPI application
├── requirements.txt             # Python dependencies
├── backend_api_specification.md # Complete API documentation
├── Performance_Review_API.postman_collection.json # Postman collection
├── .env                        # Environment variables (create this)
├── alembic/                    # Database migrations (created after alembic init)
└── alembic.ini                 # Alembic configuration (created after alembic init)
```

## Key Features Implemented

### Authentication
- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control

### Database Models
- Users (with roles: Employee, Mentor, HR Lead, System Administrator, People Committee)
- Performance Cycles
- Reviewer Selections
- Feedback Forms

### API Endpoints
- Authentication (login, logout, refresh)
- User management
- Performance cycle management
- Reviewer selection (for employees)
- Mentor approval workflow
- Feedback management (for reviewers)
- Dashboard statistics

## Development Notes

### Adding New Endpoints
1. Define the Pydantic model for request/response
2. Create the endpoint function with proper decorators
3. Add authentication and authorization checks
4. Implement database operations
5. Add error handling

### Security Considerations
- All endpoints (except login) require JWT authentication
- Role-based access control implemented
- Password hashing with bcrypt
- CORS configured for frontend integration

### Error Handling
- Standard HTTP status codes
- Detailed error messages
- Validation using Pydantic models

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Database connection issues**:
   - Check DATABASE_URL in .env file
   - Ensure SQL Server is running
   - Verify database credentials
   - Check ODBC driver installation
   - Test connection with: `python -c "import pyodbc; pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=database;UID=username;PWD=password')"`

3. **Import errors**:
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

4. **CORS issues**:
   - Update ALLOWED_ORIGINS in .env file
   - Check frontend URL configuration

### Logs
The application logs to the console. For production, consider using a proper logging configuration.

## Next Steps

1. **Implement missing business logic**:
   - Mentor-mentee relationship management
   - Notification system
   - Email integration
   - File upload for attachments

2. **Add comprehensive testing**:
   - Unit tests for models and utilities
   - Integration tests for API endpoints
   - End-to-end tests

3. **Production deployment**:
   - Use a production WSGI server (Gunicorn)
   - Set up reverse proxy (Nginx)
   - Configure SSL/TLS
   - Set up monitoring and logging

4. **Performance optimization**:
   - Database indexing
   - Caching (Redis)
   - Connection pooling
   - Query optimization

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the backend specification document
3. Check the troubleshooting section above
4. Create an issue in the repository

## License

This project is part of the Performance Review System.
