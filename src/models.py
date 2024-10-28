from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
import datetime

class Income(Base):
    __tablename__ = "incomes"
    income_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    income_amt = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)
    description = Column(String)
    account_id = Column(Integer, ForeignKey("bank_accounts.account_id"))
    category_id = Column(Integer)
    account = relationship("BankAccount", back_populates="incomes")

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    balance = Column(DECIMAL, nullable=False)
    name_of_bank = Column(String, nullable=False)
    account_no = Column(String, nullable=False, unique=True)
    incomes = relationship("Income", back_populates="account")
