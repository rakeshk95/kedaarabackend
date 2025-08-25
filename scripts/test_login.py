#!/usr/bin/env python3
"""
Test script to verify login functionality for all users.
"""

import requests
import json

# Test credentials
test_users = [
    {
        "name": "Admin User",
        "email": "admin@kedaara.com",
        "password": "Admin@123",
        "role": "System Administrator"
    },
    {
        "name": "HR Lead",
        "email": "hr.lead@kedaara.com",
        "password": "HR@123",
        "role": "HR Lead"
    },
    {
        "name": "Employee",
        "email": "employee@kedaara.com",
        "password": "Emp@123",
        "role": "Employee"
    },
    {
        "name": "Mentor",
        "email": "mentor@kedaara.com",
        "password": "Mentor@123",
        "role": "Mentor"
    },
    {
        "name": "People Committee",
        "email": "committee@kedaara.com",
        "password": "Committee@123",
        "role": "People Committee"
    }
]

def test_login():
    """Test login for all users."""
    
    base_url = "http://localhost:8000"
    login_url = f"{base_url}/api/v1/auth/login"
    
    print("🔐 Testing Login Functionality")
    print("=" * 50)
    
    for user in test_users:
        print(f"\n👤 Testing: {user['name']} ({user['role']})")
        print(f"   Email: {user['email']}")
        
        try:
            # Prepare login data
            login_data = {
                "email": user["email"],
                "password": user["password"]
            }
            
            # Make login request
            response = requests.post(
                login_url,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # Login successful
                result = response.json()
                print(f"   ✅ Login SUCCESSFUL!")
                print(f"   🔑 Access Token: {result['access_token'][:50]}...")
                print(f"   📋 Token Type: {result['token_type']}")
                print(f"   👤 User ID: {result['user']['id']}")
                print(f"   🏷️  User Role: {result['user']['role']}")
                
                # Test a protected endpoint
                test_protected_endpoint(base_url, result['access_token'], user['name'])
                
            else:
                # Login failed
                print(f"   ❌ Login FAILED!")
                print(f"   📊 Status Code: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   📝 Error: {error_detail.get('detail', 'Unknown error')}")
                except:
                    print(f"   📝 Error: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error: Make sure the server is running on {base_url}")
            break
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Login Testing Complete!")

def test_protected_endpoint(base_url, token, user_name):
    """Test accessing a protected endpoint."""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test getting user profile
        profile_url = f"{base_url}/api/v1/users/me"
        response = requests.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            print(f"   🔒 Protected endpoint test: ✅ SUCCESS")
        else:
            print(f"   🔒 Protected endpoint test: ❌ FAILED (Status: {response.status_code})")
            
    except Exception as e:
        print(f"   🔒 Protected endpoint test: ❌ ERROR - {str(e)}")

if __name__ == "__main__":
    test_login()
