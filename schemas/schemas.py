from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, root_validator
import uuid

class Login(BaseModel):
    name: str
    password: str


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Include password only for user creation

class UserResponse(UserBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True


class IncomeBase(BaseModel):
    income_amt: float
    date: datetime
    description: Optional[Union[str, None]] = None
    account_id: int
    category_id: int = 1

class IncomeCreate(BaseModel):
    name_of_bank: str
    income_amt: float
    date: datetime
    description: Optional[Union[str, None]] = None
    category_id: int = 1

class Income(IncomeBase):
    income_id: int
    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    expense_amt: float
    date: datetime
    description: Optional[str] = None
    account_id: int
    category_id: int = 2

class ExpenseCreate(BaseModel):
    name_of_bank: str
    expense_amt: float
    date: datetime
    description: Optional[str] = None
    category_id: int = 2

class Expense(ExpenseBase):
    expense_id: int
    class Config:
        from_attributes = True

class BankAccountBase(BaseModel):
    balance: float
    name_of_bank: str

class BankAccountCreate(BaseModel):
    balance: float
    name_of_bank: str
    #user_id: uuid.UUID  # Reference user ID instead of email

class BankAccount(BankAccountBase):
    account_id: int
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    category_type: str

class CategoryCreate(BaseModel):
    category_type: str

    @root_validator(pre=True)
    def check_category_type(cls, values):
        category_type = values.get("category_type")
        if category_type not in ["Income", "Expense"]:
            raise ValueError("category_type must be either 'Income' or 'Expense'")
        return values

class Category(CategoryBase):
    category_id: int
    class Config:
        from_attributes = True
