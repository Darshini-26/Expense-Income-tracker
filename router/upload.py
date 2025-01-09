from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from service.unit_of_work import UnitOfWork
from service.upload_service import upload_data_to_s3
from models import models
from typing import List
from config.database import get_db, SessionLocal 

router = APIRouter(tags=["Upload"])

# Dependency to provide a Unit of Work
def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)  # Provide session to UOW

@router.get("/income/upload")
def upload_income_data_to_s3(uow: UnitOfWork = Depends(get_uow)):
    
    try:
        # Using the UnitOfWork context manager
        with uow:
            file_url = upload_data_to_s3(uow, models.Income, "incomes.csv")
        
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/expense/upload")
def upload_expense_data_to_s3(uow: UnitOfWork = Depends(get_uow)):
    """
    Uploads expense data as a CSV file to an S3 bucket.
    """
    try:
        # Using the UnitOfWork context manager
        with uow:
            file_url = upload_data_to_s3(uow, models.Expense, "expenses.csv")
        
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bank_accounts/upload")
def upload_bank_accounts_to_s3(uow: UnitOfWork = Depends(get_uow)):
    """
    Uploads all bank accounts to S3 in a CSV format.
    """
    try:
        # Using the UnitOfWork context manager
        with uow:
            file_url = upload_data_to_s3(uow, models.BankAccount, "bankaccounts.csv")
        
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories/upload")
def upload_category_to_s3(uow: UnitOfWork = Depends(get_uow)):
    """
    Uploads all categories to S3 in CSV format.
    """
    try:
        # Using the UnitOfWork context manager
        with uow:
            file_url = upload_data_to_s3(uow, models.Category, "categories.csv")
        
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
