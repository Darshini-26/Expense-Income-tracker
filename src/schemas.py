
from pydantic import BaseModel, EmailStr, root_validator
from datetime import datetime
from typing import Optional, Union
import uuid

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: uuid.UUID
    name: str
    email: str

    class Config:
        from_attributes = True

class IncomeBase(BaseModel):
    # user_id: int
    income_amt: float
    date: datetime
    description: Optional[Union[str,None]] = None
    account_id: int
    category_id:int= 1

class IncomeCreate(BaseModel):
    email: EmailStr
    income_amt: float
    date: datetime
    description: Optional[Union[str,None]] = None
    account_id: int
    category_id: int=1

class Income(IncomeBase):
    income_id: int
    #user_id: uuid.UUID

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    # user_id: int
    expense_amt: float
    date: datetime
    description: Optional[str] = None
    account_id: int
    category_id:int= 2

class ExpenseCreate(BaseModel):
    email: EmailStr
    expense_amt: float
    date: datetime
    description: Optional[str] = None
    account_id: int
    category_id: int=2

class Expense(ExpenseBase):
    expense_id: int
    #user_id: uuid.UUID 

    class Config:
        from_attributes = True


class BankAccountBase(BaseModel):
    # user_id: int
    balance: float
    name_of_bank: str
    
class BankAccountCreate(BaseModel):
    balance: float
    name_of_bank: str
    email: str
   
class BankAccount(BankAccountBase):
    account_id: int
    #account_no:int
    #user_id: uuid.UUID

    class Config:
        from_attributes = True
        

class CategoryBase(BaseModel):
    # user_id: int
    category_type: str  

class CategoryCreate(BaseModel):
    category_type: str 

    @root_validator(pre=True)
    def check_category_type(cls, values):
        category_type = values.get('category_type')
        if category_type not in ["Income", "Expense"]:
            raise ValueError("category_type must be either 'Income' or 'Expense'")
        return values

class Category(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True

