# service/income_service.py
from sqlalchemy.orm import Session
from repository.income_repository import IncomeRepository
from utils.income_utils import create_new_income
from models.models import Income, BankAccount
from fastapi import HTTPException
from schemas.schemas import IncomeCreate

class IncomeService:
    @staticmethod
    def create_income_service(db: Session, income:IncomeCreate) -> Income:
        """Handles business logic for creating a new income."""
        bank_account = db.query(BankAccount).filter(
        BankAccount.name_of_bank == income.name_of_bank
    ).first()
        if not bank_account:
            raise HTTPException(status_code=404, detail="Bank account not found")
        db_income = Income(
        user_id=bank_account.user_id,
        income_amt=income.income_amt,
        date=income.date,
        description=income.description,
        account_id=bank_account.account_id,
        category_id=income.category_id,
    )
        return IncomeRepository.create_income(db,db_income)
        

    @staticmethod
    def get_income_by_id_service(db: Session, income_id: int) -> Income:
        """Handles business logic for fetching income by ID."""
        income = IncomeRepository.get_income_by_id(db, income_id)
        if not income:
            raise ValueError("Income not found.")
        return income

    @staticmethod
    def get_all_incomes_service(db: Session):
        """Handles business logic for fetching all incomes."""
        return IncomeRepository.get_all_incomes(db)

    @staticmethod
    def update_income_service(db: Session, income_id: int, income: IncomeCreate):
        db_income = db.query(Income).filter(Income.income_id == income_id).first()
        if not db_income:
            raise HTTPException(status_code=404, detail="Income not found")

        bank_account = db.query(BankAccount).filter(
            BankAccount.name_of_bank == income.name_of_bank
        ).first()
        if not bank_account:
            raise HTTPException(status_code=404, detail="Bank account not found")

        db_income.income_amt = income.income_amt
        db_income.date = income.date
        db_income.description = income.description
        db_income.account_id = bank_account.account_id
        db_income.category_id = income.category_id

        return IncomeRepository.update_income(db,db_income)

    @staticmethod
    def delete_income_service(db: Session, income_id: int):
        return IncomeRepository.delete_income(db, income_id)