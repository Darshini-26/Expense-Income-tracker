from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.bank_account_service import BankAccountService
from config.database import get_db, SessionLocal
from schemas.schemas import BankAccount, BankAccountCreate
from typing import List
from service.unit_of_work import UnitOfWork

router = APIRouter(prefix="/bankaccount", tags=["BankAccount"])

# Dependency to provide a Unit of Work
def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)

# Create a new Bank Account
@router.post("/", response_model=BankAccount)
def create_bank_account(bank_account: BankAccountCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return BankAccountService.create_bank_account_service(uow, bank_account)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Fetch Bank Account by ID
@router.get("/{account_id}", response_model=BankAccount)
def read_bank_account(account_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        return BankAccountService.get_bank_account_by_id_service(uow, account_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Fetch all Bank Accounts
@router.get("/", response_model=List[BankAccount])
def read_bank_accounts(uow: UnitOfWork = Depends(get_uow)):
    return BankAccountService.get_all_bank_accounts_service(uow)


# Update Bank Account by ID
@router.put("/{account_id}", response_model=BankAccount)
def update_bank_account(account_id: int, bank_account: BankAccountCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        return BankAccountService.update_bank_account_service(uow, account_id, bank_account)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete Bank Account by ID
@router.delete("/{account_id}", response_model=dict)
def delete_bank_account(account_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        success = BankAccountService.delete_bank_account_service(uow, account_id)
        if not success:
            raise HTTPException(status_code=404, detail="Bank account not found")
        return {"message": "Bank account deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
