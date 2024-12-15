from fastapi import FastAPI, HTTPException
from typing import List
from fastapi import Depends
from src.database import SessionLocal, engine
import src.models as models
import src.schemas as schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# INCOME
@app.post("/income/", tags=["INCOME"], response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    db_income = models.Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income



@app.get("/income/", tags=["INCOME"], response_model=List[schemas.Income])
def read_income(db: Session = Depends(get_db)):
    db_income = db.query(models.Income).all()
    return db_income


@app.get("/income/{income_id}", tags=["INCOME"], response_model=schemas.Income)
def read_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income


@app.put("/income/{income_id}", tags=["INCOME"], response_model=schemas.Income)
def update_income(income_id: int, income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    db_income.user_id = income.user_id
    db_income.income_amt = income.income_amt
    db_income.description = income.description
    db_income.account_id = income.account_id
    db_income.category_id = income.category_id
    db.commit()
    db.refresh(db_income)
    return db_income


@app.delete("/income/{income_id}", tags=["INCOME"])
def delete_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    db.delete(db_income)
    db.commit()
    return {"Message": "Records deleted"}


# EXPENSE
@app.post("/expense/", tags=["EXPENSE"], response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense



@app.get("/expense/", tags=["EXPENSE"], response_model=List[schemas.Expense])
def read_expense(db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).all()
    return db_expense


@app.get("/expense/{expense_id}", tags=["EXPENSE"], response_model=schemas.Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@app.put("/expense/{expense_id}", tags=["EXPENSE"], response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.user_id = expense.user_id
    db_expense.expense_amt = expense.expense_amt
    db_expense.description = expense.description
    db_expense.account_id = expense.account_id
    db_expense.category_id = expense.category_id
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expense/{expense_id}", tags=["EXPENSE"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"Message": "Records deleted"}


# BANK ACCOUNT
@app.post("/bank_account/", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def create_bank_account(bank_account: schemas.BankAccountCreate, db: Session = Depends(get_db)):
    db_account = models.BankAccount(**bank_account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@app.get("/bank_account/", tags=["BANK ACCOUNT"], response_model=List[schemas.BankAccount])
def read_bank_account(db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).all()
    return db_account


@app.get("/bank_account/{account_id}", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def read_bank_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return db_account


@app.put("/bank_account/{account_id}", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def update_bank_account(account_id: int, bank_account: schemas.BankAccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db_account.user_id = bank_account.user_id
    db_account.balance = bank_account.balance
    db_account.name_of_bank = bank_account.name_of_bank
    db_account.account_no = bank_account.account_no
    db.commit()
    db.refresh(db_account)
    return db_account


@app.delete("/bank_account/{account_id}", tags=["BANK ACCOUNT"])
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db.delete(db_account)
    db.commit()
    return {"Message": "Records deleted"}

# CATEGORY
@app.post("/categories/", tags=["CATEGORY"], response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories/", tags=["CATEGORY"], response_model=List[schemas.Category])
def read_category(db: Session = Depends(get_db)):
    db_category = db.query(models.Category).all()
    return db_category


@app.get("/categories/{category_id}", tags=["CATEGORY"], response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.put("/categories/{category_id}", tags=["CATEGORY"], response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.user_id = category.user_id
    db_category.category_type = category.category_type
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}", tags=["CATEGORY"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"Message": "Records deleted"}
