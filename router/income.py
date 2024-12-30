# router/income.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.income_service import IncomeService
from config.database import get_db  # Assuming this is your database session
from schemas.schemas import Income, IncomeCreate
from typing import List

router = APIRouter( tags=["Income"])

@router.post("/income/",response_model=Income)
def create_income(income:IncomeCreate, db: Session = Depends(get_db)):
    try:
        return IncomeService.create_income_service(db, income)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/income/{income_id}",response_model=Income)
def read_income(income_id: int, db: Session = Depends(get_db)):
    try:
        return IncomeService.get_income_by_id_service(db, income_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/incomes/",response_model=List[Income])
def read_incomes(db: Session = Depends(get_db)):
    return IncomeService.get_all_incomes_service(db)

@router.put("/income/",response_model=Income)
def update_incomes(income_id:int,income:IncomeCreate,db:Session=Depends(get_db)):
    return IncomeService.update_income_service(db,income_id,income)

@router.delete("/income/")
def delete_incomes(income_id:int,db:Session=Depends(get_db)):
    return IncomeService.delete_income_service(db,income_id)