from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.bank_account_service import BankAccountService
from config.database import get_db
from schemas.schemas import BankAccount, BankAccountCreate
from typing import List

router = APIRouter(tags=["BankAccount"])

@router.post("/bankaccount/", response_model=BankAccount)
def create_bank_account(bank_account: BankAccountCreate, db: Session = Depends(get_db)):
    try:
        return BankAccountService.create_bank_account_service(db, bank_account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bankaccount/{account_id}", response_model=BankAccount)
def read_bank_account(account_id: int, db: Session = Depends(get_db)):
    try:
        return BankAccountService.get_bank_account_by_id_service(db, account_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/bankaccounts/", response_model=List[BankAccount])
def read_bank_accounts(db: Session = Depends(get_db)):
    return BankAccountService.get_all_bank_accounts_service(db)

@router.put("/bankaccount/{account_id}", response_model=BankAccount)
def update_bank_account(account_id: int, bank_account: BankAccountCreate, db: Session = Depends(get_db)):
    return BankAccountService.update_bank_account_service(db, account_id, bank_account)

@router.delete("/bankaccount/")
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    return BankAccountService.delete_bank_account_service(db, account_id)
