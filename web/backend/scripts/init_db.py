import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from alembic import command
from alembic.config import Config
from app.core.config import settings
from app.models.audio import Base, init_db

def init_alembic():
    """Initialize Alembic configuration"""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)
    return alembic_cfg

def create_database():
    """Create database and initialize tables"""
    # Create engine without database name to connect to PostgreSQL server
    engine_url = settings.SQLALCHEMY_DATABASE_URI.rsplit('/', 1)[0]
    temp_engine = create_engine(engine_url)
    
    # Create database if it doesn't exist
    with temp_engine.connect() as conn:
        conn.execute("commit")
        try:
            conn.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print(f"Created database: {settings.POSTGRES_DB}")
        except Exception as e:
            print(f"Database already exists or error: {e}")

def setup_database():
    """Set up database schema and initial data"""
    try:
        # Create main engine
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        
        # Create all tables
        print("Creating database tables...")
        init_db(engine)
        
        # Initialize Alembic
        print("Initializing Alembic...")
        alembic_cfg = init_alembic()
        command.stamp(alembic_cfg, "head")
        
        print("Database initialization completed successfully")
        return True
    except Exception as e:
        print(f"Error during database setup: {e}")
        return False

if __name__ == "__main__":
    print("Starting database initialization...")
    create_database()
    if setup_database():
        print("Database setup completed successfully")
    else:
        print("Database setup failed")

