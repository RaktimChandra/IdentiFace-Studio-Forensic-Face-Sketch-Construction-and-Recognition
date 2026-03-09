"""
Database initialization script
Creates all tables and sets up the database schema
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

def init_db():
    """Initialize database tables"""
    print(f"Initializing database: {settings.DATABASE_URL}")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
