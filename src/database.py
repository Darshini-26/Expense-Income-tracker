from sqlalchemy import create_engine,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import src.config as config


DATABASE_URL = config.get_ssm_parameter('database_url')

if not DATABASE_URL:
    raise RuntimeError("Failed to retrieve the database URL from SSM.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 10} )

with engine.connect() as connection:
    # Use `text` to mark the SQL query explicitly
    result = connection.execute(text("SELECT 1"))
    print(result.fetchone())
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()