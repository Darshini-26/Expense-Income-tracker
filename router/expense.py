# router/expense.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.expense_service import ExpenseService
from config.database import get_db  # Assuming this is your database session
from schemas.schemas import Expense, ExpenseCreate
from typing import List

router = APIRouter(tags=["Expense"])

@router.post("/expense/", response_model=Expense)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return ExpenseService.create_expense_service(db, expense)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/expense/{expense_id}", response_model=Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    try:
        return ExpenseService.get_expense_by_id_service(db, expense_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/expenses/", response_model=List[Expense])
def read_expenses(db: Session = Depends(get_db)):
    return ExpenseService.get_all_expenses_service(db)

@router.put("/expense/", response_model=Expense)
def update_expenses(expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    return ExpenseService.update_expense_service(db, expense_id, expense)

@router.delete("/expense/")
def delete_expenses(expense_id: int, db: Session = Depends(get_db)):
    return ExpenseService.delete_expense_service(db, expense_id)
