#!/usr/bin/env python3
"""
Script to create users for the Performance Review System.
This creates an admin user and sample users for testing.
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

def create_all_users():
    """Create admin user and sample users."""
    
    # Create database tables if they don't exist
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("🚀 Creating users for Performance Review System...")
        print("=" * 60)
        
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
        
        # Create sample users
        hr_lead = User(
            email="hr.lead@kedaara.com",
            name="HR Lead",
            role="HR Lead",
            department="Human Resources",
            position="HR Lead",
            password_hash=get_password_hash("HR@123"),
            is_active=True
        )
        
        employee = User(
            email="employee@kedaara.com",
            name="John Employee",
            role="Employee",
            department="Engineering",
            position="Software Developer",
            password_hash=get_password_hash("Emp@123"),
            is_active=True
        )
        
        mentor = User(
            email="mentor@kedaara.com",
            name="Sarah Mentor",
            role="Mentor",
            department="Engineering",
            position="Senior Developer",
            password_hash=get_password_hash("Mentor@123"),
            is_active=True
        )
        
        committee_member = User(
            email="committee@kedaara.com",
            name="Mike Committee",
            role="People Committee",
            department="Management",
            position="Committee Member",
            password_hash=get_password_hash("Committee@123"),
            is_active=True
        )
        
        # Add all users
        users = [admin_user, hr_lead, employee, mentor, committee_member]
        
        for user in users:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if not existing_user:
                db.add(user)
                print(f"✅ Created user: {user.email} ({user.role})")
            else:
                print(f"⚠️  User already exists: {user.email}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("📋 LOGIN CREDENTIALS")
        print("=" * 60)
        print()
        print("🔐 ADMIN USER:")
        print(f"   Email: admin@kedaara.com")
        print(f"   Password: Admin@123")
        print(f"   Role: System Administrator")
        print()
        print("👥 HR LEAD:")
        print(f"   Email: hr.lead@kedaara.com")
        print(f"   Password: HR@123")
        print(f"   Role: HR Lead")
        print()
        print("👤 EMPLOYEE:")
        print(f"   Email: employee@kedaara.com")
        print(f"   Password: Emp@123")
        print(f"   Role: Employee")
        print()
        print("🎓 MENTOR:")
        print(f"   Email: mentor@kedaara.com")
        print(f"   Password: Mentor@123")
        print(f"   Role: Mentor")
        print()
        print("🏛️  PEOPLE COMMITTEE:")
        print(f"   Email: committee@kedaara.com")
        print(f"   Password: Committee@123")
        print(f"   Role: People Committee")
        print()
        print("=" * 60)
        print("⚠️  IMPORTANT:")
        print("- Change passwords after first login")
        print("- Keep these credentials secure")
        print("- Use admin account to manage the system")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_all_users()
