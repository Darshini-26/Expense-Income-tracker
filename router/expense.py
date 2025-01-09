from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas.schemas import Expense, ExpenseCreate
from service.expense_service import ExpenseService
from config.database import get_db, SessionLocal
from service.unit_of_work import UnitOfWork

router = APIRouter(prefix="/expense", tags=["Expense"])

# Dependency to provide a Unit of Work
def get_uow() -> UnitOfWork:
    # Pass SessionLocal as a callable to create a new session for each request
    return UnitOfWork(SessionLocal)

# Fetch all Expense records
@router.get("/", response_model=List[Expense])
def get_all_expenses(uow: UnitOfWork = Depends(get_uow)):
    try:
        return ExpenseService.get_all_expenses_service(uow)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fetch Expense by ID
@router.get("/{id}", response_model=Expense)
def get_expense_by_id(id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        expense = ExpenseService.get_expense_by_id_service(uow, id)  # Ensure the right parameter is passed
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new Expense record
@router.post("/", response_model=Expense)
def create_expense(expense: ExpenseCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return ExpenseService.create_expense_service(uow, expense)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Expense record by ID
@router.put("/{id}", response_model=Expense)
def update_expense(id: int, updated_expense: ExpenseCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        updated = ExpenseService.update_expense_service(uow, id, updated_expense)
        if not updated:
            raise HTTPException(status_code=404, detail="Expense not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Expense record by ID
@router.delete("/{id}", response_model=dict)
def delete_expense(id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        success = ExpenseService.delete_expense_service(uow, id)
        if not success:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {"message": "Expense deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
