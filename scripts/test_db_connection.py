#!/usr/bin/env python3
"""
Test script to verify database connection.
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings


def test_database_connection():
    """Test the database connection."""
    print("🔍 Testing database connection...")
    print(f"Database URL: {settings.database_url}")
    
    try:
        # Create engine
        engine = create_engine(
            settings.database_url,
            echo=True,  # Enable SQL logging for debugging
            connect_args={
                "TrustServerCertificate": "yes",
                "Encrypt": "yes",
            }
        )
        
        # Test connection
        with engine.connect() as connection:
            print("✅ Successfully connected to database!")
            
            # Test a simple query
            result = connection.execute(text("SELECT @@VERSION as version"))
            version = result.fetchone()
            print(f"✅ SQL Server Version: {version[0]}")
            
            # Test database name
            result = connection.execute(text("SELECT DB_NAME() as database_name"))
            db_name = result.fetchone()
            print(f"✅ Connected to database: {db_name[0]}")
            
            # Test if we can create tables (check permissions)
            print("✅ Database connection test completed successfully!")
            
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n🎉 Database connection test passed!")
        print("You can now run the application with:")
        print("  make run-dev")
    else:
        print("\n💥 Database connection test failed!")
        print("Please check your database configuration and try again.")
        sys.exit(1)
