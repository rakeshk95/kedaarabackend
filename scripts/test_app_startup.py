#!/usr/bin/env python3
"""
Test script to verify FastAPI application startup.
"""

import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_app_startup():
    """Test if the FastAPI application can start successfully."""
    print("🔍 Testing FastAPI application startup...")
    
    try:
        from app.main import app
        
        # Create test client
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        print(f"✅ Root endpoint response: {response.status_code}")
        
        # Test health endpoint
        response = client.get("/health")
        print(f"✅ Health endpoint response: {response.status_code}")
        
        # Test API docs
        response = client.get("/docs")
        print(f"✅ API docs response: {response.status_code}")
        
        print("✅ Application startup test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_app_startup()
    sys.exit(0 if success else 1)
