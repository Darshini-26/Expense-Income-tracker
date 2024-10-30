from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import src.config as config

DATABASE_URL = config.DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={
    "check_same_thread": False
})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()