from config.database import Base
from sqlalchemy import (
    Column, Integer, String, DECIMAL, DateTime, ForeignKey, BigInteger, UniqueConstraint
)
from config.database import Base

class User_auth(Base):
    __tablename__ = "User_auth"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
