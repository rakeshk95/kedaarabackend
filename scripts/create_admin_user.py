#!/usr/bin/env python3
"""
Script to create the first admin user for the Performance Review System.
This should be run once to set up the initial administrator account.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.core.config import settings

def create_admin_user():
    """Create the first admin user."""
    
    # Create database tables if they don't exist
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.role == "System Administrator").first()
        if existing_admin:
            print("❌ Admin user already exists!")
            print(f"Email: {existing_admin.email}")
            print("Please use the existing admin account or contact your system administrator.")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@kedaara.com",
            name="System Administrator",
            role="System Administrator",
            department="IT",
            position="System Administrator",
            password_hash=get_password_hash("Admin@123"),
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print("\n📋 Login Credentials:")
        print("=" * 40)
        print(f"Email: {admin_user.email}")
        print(f"Password: Admin@123")
        print(f"Role: {admin_user.role}")
        print("=" * 40)
        print("\n⚠️  IMPORTANT:")
        print("- Change the password after first login")
        print("- Keep these credentials secure")
        print("- This is the only admin account that can manage the system")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_users():
    """Create sample users for testing different roles."""
    
    db = SessionLocal()
    try:
        # Sample HR Lead
        hr_lead = User(
            email="hr.lead@kedaara.com",
            name="HR Lead",
            role="HR Lead",
            department="Human Resources",
            position="HR Lead",
            password_hash=get_password_hash("HR@123"),
            is_active=True
        )
        
        # Sample Employee
        employee = User(
            email="employee@kedaara.com",
            name="John Employee",
            role="Employee",
            department="Engineering",
            position="Software Developer",
            password_hash=get_password_hash("Emp@123"),
            is_active=True
        )
        
        # Sample Mentor
        mentor = User(
            email="mentor@kedaara.com",
            name="Sarah Mentor",
            role="Mentor",
            department="Engineering",
            position="Senior Developer",
            password_hash=get_password_hash("Mentor@123"),
            is_active=True
        )
        
        # Sample People Committee Member
        committee_member = User(
            email="committee@kedaara.com",
            name="Mike Committee",
            role="People Committee",
            department="Management",
            position="Committee Member",
            password_hash=get_password_hash("Committee@123"),
            is_active=True
        )
        
        users = [hr_lead, employee, mentor, committee_member]
        
        for user in users:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if not existing_user:
                db.add(user)
                print(f"✅ Created user: {user.email} ({user.role})")
            else:
                print(f"⚠️  User already exists: {user.email}")
        
        db.commit()
        
        print("\n📋 Sample User Credentials:")
        print("=" * 50)
        print("HR Lead:")
        print(f"  Email: {hr_lead.email}")
        print(f"  Password: HR@123")
        print()
        print("Employee:")
        print(f"  Email: {employee.email}")
        print(f"  Password: Emp@123")
        print()
        print("Mentor:")
        print(f"  Email: {mentor.email}")
        print(f"  Password: Mentor@123")
        print()
        print("People Committee:")
        print(f"  Email: {committee_member.email}")
        print(f"  Password: Committee@123")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error creating sample users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Performance Review System - User Setup")
    print("=" * 50)
    
    choice = input("\nChoose an option:\n1. Create Admin User Only\n2. Create Admin + Sample Users\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_admin_user()
    elif choice == "2":
        create_admin_user()
        print("\n" + "=" * 50)
        create_sample_users()
    else:
        print("❌ Invalid choice. Please run the script again.")
