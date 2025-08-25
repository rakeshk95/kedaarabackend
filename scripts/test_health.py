#!/usr/bin/env python3
"""
Test script to verify health endpoints.
"""

import requests
import json

def test_health_endpoints():
    """Test health check endpoints."""
    
    base_url = "http://localhost:8000"
    
    print("🏥 Testing Health Endpoints")
    print("=" * 50)
    
    # Test basic health check
    try:
        response = requests.get(f"{base_url}/api/v1/health")
        print(f"\n🔍 Basic Health Check:")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {result.get('status')}")
            print(f"   🕐 Timestamp: {result.get('timestamp')}")
            print(f"   🏷️  Service: {result.get('service')}")
            print(f"   📦 Version: {result.get('version')}")
            print(f"   🌍 Environment: {result.get('environment')}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test detailed health check
    try:
        response = requests.get(f"{base_url}/api/v1/health/detailed")
        print(f"\n🔍 Detailed Health Check:")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {result.get('status')}")
            print(f"   🗄️  Database: {result.get('database', {}).get('status')}")
            print(f"   🔧 Features: {result.get('features')}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Health Testing Complete!")

if __name__ == "__main__":
    test_health_endpoints()
