#!/bin/bash

# FastAPI Project Setup Script
# This script sets up the development environment for the FastAPI project

set -e

echo "🚀 Setting up FastAPI Project with SQL Server..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.11 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your database configuration"
else
    echo "✅ .env file already exists"
fi

# Initialize Alembic if not already done
if [ ! -d "alembic/versions" ]; then
    echo "🗄️ Initializing Alembic..."
    alembic init alembic
    echo "⚠️  Please update alembic.ini with your database URL"
else
    echo "✅ Alembic already initialized"
fi

# Create initial migration if no migrations exist
if [ ! "$(ls -A alembic/versions 2>/dev/null)" ]; then
    echo "📝 Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
    echo "⚠️  Please review the migration file before applying"
else
    echo "✅ Migrations already exist"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database configuration"
echo "2. Run 'alembic upgrade head' to apply migrations"
echo "3. Run 'make run-dev' to start the development server"
echo "4. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "Available commands:"
echo "  make help          - Show all available commands"
echo "  make run-dev       - Start development server"
echo "  make test          - Run tests"
echo "  make format        - Format code"
echo "  make lint          - Run linting"
echo ""
