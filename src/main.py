from fastapi import FastAPI
from typing import List
from fastapi import Depends
from src.database import SessionLocal, engine
import src.models as models
from fastapi import Response
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


@app.post("/income/", response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    db_income = models.Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


@app.get("/income/", response_model=List[schemas.Income])
def read_income(db: Session = Depends(get_db)):
    db_income = db.query(models.Income).all()
    if not db_income:
        return []
    return db_income

@app.put("/income/{income_id}", response_model=schemas.Income)
def update_income(income_id: int, income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id==income_id).first()
    db_income.user_id = income.user_id
    db_income.income_amt = income.income_amt
    db_income.description = income.description
    db_income.account_id = income.account_id
    db_income.category_id = income.category_id
    db.commit()
    db.refresh(db_income)
    return db_income

@app.delete("/income/{income_id}")
def delete_income(income_id:int , db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id==income_id).first()
    if db_income:
        db.delete(db_income)
        db.commit()
        return {"Message":"Records deleted"}
    return {"Message":"ID not available"}


@app.post("/expense/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expense/", response_model=List[schemas.Expense])
def read_expense(db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).all()
    if not db_expense:
        return []
    return db_expense

@app.put("/expense/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id==expense_id).first()
    db_expense.user_id = expense.user_id
    db_expense.expense_amt = expense.expense_amt
    db_expense.description = expense.description
    db_expense.account_id = expense.account_id
    db_expense.category_id = expense.category_id
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/expense/{expense_id}")
def delete_expense(expense_id:int , db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id==expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
        return {"Message":"Records deleted"}
    return {"Message":"ID not available"}