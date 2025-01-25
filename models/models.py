from datetime import datetime
import random
import uuid
from sqlalchemy import (
    Column, Integer, String, DECIMAL, DateTime, ForeignKey, BigInteger, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base, engine


def generate_account_no():
    """
    Generate a random 16-digit account number.
    """
    return random.randint(10**15, 10**16 - 1)


# User Table
class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="user")
    #categories = relationship("Category", back_populates="user")
    incomes = relationship("Income", back_populates="user")
    expenses = relationship("Expense", back_populates="user")


# Income Table
class Income(Base):
    __tablename__ = "incomes"

    income_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)  # Use UUID
    income_amt = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey("bank_accounts.account_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False, default=1)

    # Relationships
    user = relationship("User", back_populates="incomes")
    account = relationship("BankAccount", back_populates="incomes")
    category = relationship("Category", back_populates="incomes")


class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)  # Use UUID
    expense_amt = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey("bank_accounts.account_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False, default=2)

    # Relationships
    user = relationship("User", back_populates="expenses")
    account = relationship("BankAccount", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")


# BankAccount Table
class BankAccount(Base):
    __tablename__ = "bank_accounts"

    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)  # Use UUID
    balance = Column(DECIMAL(10, 2), nullable=False)
    name_of_bank = Column(String, nullable=False, unique=True)
    account_no = Column(BigInteger, unique=True, default=generate_account_no)

    # Enforce unique constraint for name_of_bank
    __table_args__ = (UniqueConstraint("user_id", "name_of_bank", name="uq_name_of_bank"),)

    # Relationships
    user = relationship("User", back_populates="bank_accounts")
    expenses = relationship("Expense", back_populates="account")
    incomes = relationship("Income", back_populates="account")


# Category Table
class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    #user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)  # Use UUID
    category_type = Column(String, nullable=False)

    # Relationships
    #user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")
    incomes = relationship("Income", back_populates="category")


Base.metadata.create_all(bind=engine)
