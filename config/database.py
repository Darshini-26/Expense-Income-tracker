from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import config.config as config
# from contextlib import contextmanager

# Retrieve the DATABASE_URL from config.py (via SSM)
DATABASE_URL = config.get_database_url()

if not DATABASE_URL:
    raise RuntimeError("Failed to retrieve the database URL from SSM.")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c statement_timeout=60000"}
)

# Test connection with a simple query
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.fetchone())

# Set up the session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# @contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure this line is not indented under the try block
