from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas.schemas import Income, IncomeCreate
from service.income_service import IncomeService
from config.database import get_db, SessionLocal
from service.unit_of_work import UnitOfWork

router = APIRouter(prefix="/income", tags=["Income"])

# Dependency to provide a Unit of Work
def get_uow() -> UnitOfWork:
    # Pass SessionLocal as a callable to create a new session for each request
    return UnitOfWork(SessionLocal)

# Fetch all Income records
@router.get("/", response_model=List[Income])
def get_all_income(uow: UnitOfWork = Depends(get_uow)):
    try:
        return IncomeService.get_all_incomes_service(uow)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fetch Income by ID
@router.get("/{id}", response_model=Income)
def get_income_by_id(id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        income = IncomeService.get_income_by_id_service(uow, id)  # Ensure the right parameter is passed
        if not income:
            raise HTTPException(status_code=404, detail="Income not found")
        return income
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new Income record
@router.post("/", response_model=Income)
def create_income(income: IncomeCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return IncomeService.create_income_service(uow, income)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Income record by ID
@router.put("/{id}", response_model=Income)
def update_income(id: int, updated_income: IncomeCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        updated = IncomeService.update_income_service(uow, id, updated_income)
        if not updated:
            raise HTTPException(status_code=404, detail="Income not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Income record by ID
@router.delete("/{id}", response_model=dict)
def delete_income(id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        success = IncomeService.delete_income_service(uow, id)
        if not success:
            raise HTTPException(status_code=404, detail="Income not found")
        return {"message": "Income deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
