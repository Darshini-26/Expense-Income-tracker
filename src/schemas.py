from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncomeBase(BaseModel):
    user_id: int
    income_amt: float
    date: datetime
    description: Optional[str] = None
    account_id: int
    category_id: int

class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    income_id: int

    class Config:
        orm_mode = True

class BankAccountBase(BaseModel):
    user_id: int
    balance: float
    name_of_bank: str
    account_no: str

class BankAccountCreate(BankAccountBase):
    pass

class BankAccount(BankAccountBase):
    account_id: int

    class Config:
        orm_mode = True
