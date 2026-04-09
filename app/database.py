# Database configuration and connection management for FastAPI backend
# Sets up SQLite database connection and session management

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Get the absolute path to the project root directory
# This ensures the database file location is consistent regardless of where the script is run from
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# SQLite database URL pointing to users.db in the project root
# Shared database file between assignments API and Flask user management
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"

# Create SQLAlchemy engine (database connection factory)
# check_same_thread=False allows multiple threads to use the same connection (needed for Flask)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory for creating database sessions
# autocommit=False: Explicit commit required for changes
# autoflush=False: Manual flush required before queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models - defines table metadata
Base = declarative_base()

# Dependency function for FastAPI to automatically provide database sessions
# Uses yield to ensure database connection is closed after each request
def get_db():
    # Create new database session
    db = SessionLocal()
    try:
        # Provide session to route handler
        yield db
    finally:
        # Always close session to prevent connection leaks
        db.close()