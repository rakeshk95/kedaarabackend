@echo off
REM FastAPI Project Setup Script for Windows
REM This script sets up the development environment for the FastAPI project

echo 🚀 Setting up FastAPI Project with SQL Server...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python version check passed: %python_version%

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️ Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit .env file with your database configuration
) else (
    echo ✅ .env file already exists
)

REM Initialize Alembic if not already done
if not exist "alembic\versions" (
    echo 🗄️ Initializing Alembic...
    alembic init alembic
    echo ⚠️  Please update alembic.ini with your database URL
) else (
    echo ✅ Alembic already initialized
)

REM Create initial migration if no migrations exist
dir /b alembic\versions\*.py >nul 2>&1
if errorlevel 1 (
    echo 📝 Creating initial migration...
    alembic revision --autogenerate -m "Initial migration"
    echo ⚠️  Please review the migration file before applying
) else (
    echo ✅ Migrations already exist
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your database configuration
echo 2. Run 'alembic upgrade head' to apply migrations
echo 3. Run 'make run-dev' to start the development server
echo 4. Visit http://localhost:8000/docs for API documentation
echo.
echo Available commands:
echo   make help          - Show all available commands
echo   make run-dev       - Start development server
echo   make test          - Run tests
echo   make format        - Format code
echo   make lint          - Run linting
echo.

pause
