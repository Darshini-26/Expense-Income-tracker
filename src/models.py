from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime

class Income(Base):
    __tablename__ = "incomes"
    
    income_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    income_amt = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey("bank_accounts.account_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
  
    account = relationship("BankAccount", back_populates="incomes")
    category = relationship("Category", back_populates="incomes")

class Expense(Base):
    __tablename__ = "expenses"
    
    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    expense_amt = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String)
    account_id = Column(Integer, ForeignKey("bank_accounts.account_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
   
    account = relationship("BankAccount", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    balance = Column(DECIMAL, nullable=False)
    name_of_bank = Column(String, nullable=False)
    account_no = Column(String, unique=True, nullable=False)
    
    expenses = relationship("Expense", back_populates="account")
    incomes = relationship("Income", back_populates="account")

class Category(Base):
    __tablename__ = "categories"
    
    category_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    category_type = Column(String, nullable=False) 
 
    expenses = relationship("Expense", back_populates="category")
    incomes = relationship("Income", back_populates="category")

