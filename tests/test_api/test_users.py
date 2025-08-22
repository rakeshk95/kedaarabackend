"""
Tests for user management endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.core.security import create_access_token


def get_auth_headers(token: str):
    """Get authorization headers."""
    return {"Authorization": f"Bearer {token}"}


def test_create_user_success(client: TestClient, db: Session, test_superuser_data: dict):
    """Test successful user creation by superuser."""
    # Create superuser first
    user_service = UserService(db)
    superuser_create = UserCreate(**test_superuser_data)
    superuser = user_service.create_user(superuser_create)
    
    # Create access token for superuser
    token = create_access_token(subject=superuser.id)
    headers = get_auth_headers(token)
    
    # Test user creation
    new_user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "full_name": "New User",
        "password": "newpassword123",
        "is_active": True,
        "is_superuser": False
    }
    
    response = client.post(
        "/api/v1/users/",
        json=new_user_data,
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_user_data["email"]
    assert data["username"] == new_user_data["username"]
    assert "password" not in data


def test_create_user_duplicate_email(client: TestClient, db: Session, test_superuser_data: dict, test_user_data: dict):
    """Test user creation with duplicate email."""
    # Create superuser
    user_service = UserService(db)
    superuser_create = UserCreate(**test_superuser_data)
    superuser = user_service.create_user(superuser_create)
    
    # Create first user
    user_create = UserCreate(**test_user_data)
    user_service.create_user(user_create)
    
    # Create access token for superuser
    token = create_access_token(subject=superuser.id)
    headers = get_auth_headers(token)
    
    # Try to create user with same email
    duplicate_user_data = test_user_data.copy()
    duplicate_user_data["username"] = "differentuser"
    
    response = client.post(
        "/api/v1/users/",
        json=duplicate_user_data,
        headers=headers
    )
    
    assert response.status_code == 400
    assert "email already exists" in response.json()["detail"]


def test_get_users_success(client: TestClient, db: Session, test_superuser_data: dict, test_user_data: dict):
    """Test successful user retrieval by superuser."""
    # Create superuser
    user_service = UserService(db)
    superuser_create = UserCreate(**test_superuser_data)
    superuser = user_service.create_user(superuser_create)
    
    # Create regular user
    user_create = UserCreate(**test_user_data)
    user_service.create_user(user_create)
    
    # Create access token for superuser
    token = create_access_token(subject=superuser.id)
    headers = get_auth_headers(token)
    
    # Test get users
    response = client.get("/api/v1/users/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # superuser + regular user


def test_get_user_by_id_success(client: TestClient, db: Session, test_superuser_data: dict, test_user_data: dict):
    """Test successful user retrieval by ID."""
    # Create superuser
    user_service = UserService(db)
    superuser_create = UserCreate(**test_superuser_data)
    superuser = user_service.create_user(superuser_create)
    
    # Create regular user
    user_create = UserCreate(**test_user_data)
    user = user_service.create_user(user_create)
    
    # Create access token for superuser
    token = create_access_token(subject=superuser.id)
    headers = get_auth_headers(token)
    
    # Test get user by ID
    response = client.get(f"/api/v1/users/{user.id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email


def test_update_user_success(client: TestClient, db: Session, test_superuser_data: dict, test_user_data: dict):
    """Test successful user update."""
    # Create superuser
    user_service = UserService(db)
    superuser_create = UserCreate(**test_superuser_data)
    superuser = user_service.create_user(superuser_create)
    
    # Create regular user
    user_create = UserCreate(**test_user_data)
    user = user_service.create_user(user_create)
    
    # Create access token for superuser
    token = create_access_token(subject=superuser.id)
    headers = get_auth_headers(token)
    
    # Test update user
    update_data = {"full_name": "Updated Name"}
    response = client.put(
        f"/api/v1/users/{user.id}",
        json=update_data,
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"


def test_delete_user_success(client: TestClient, db: Session, test_superuser_data: dict, test_user_data: dict):
    """Test successful user deletion."""
    # Create superuser
    user_service = UserService(db)
    superuser_create = UserCreate(**test_superuser_data)
    superuser = user_service.create_user(superuser_create)
    
    # Create regular user
    user_create = UserCreate(**test_user_data)
    user = user_service.create_user(user_create)
    
    # Create access token for superuser
    token = create_access_token(subject=superuser.id)
    headers = get_auth_headers(token)
    
    # Test delete user
    response = client.delete(f"/api/v1/users/{user.id}", headers=headers)
    
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
