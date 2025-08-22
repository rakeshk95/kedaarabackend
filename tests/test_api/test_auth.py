"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.user import UserCreate


def test_login_success(client: TestClient, db: Session, test_user_data: dict):
    """Test successful login."""
    # Create user first
    user_service = UserService(db)
    user_create = UserCreate(**test_user_data)
    user_service.create_user(user_create)
    
    # Test login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_inactive_user(client: TestClient, db: Session, test_user_data: dict):
    """Test login with inactive user."""
    # Create inactive user
    user_service = UserService(db)
    test_user_data["is_active"] = False
    user_create = UserCreate(**test_user_data)
    user_service.create_user(user_create)
    
    # Test login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]
