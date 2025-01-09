from fastapi import HTTPException
from models.models import Income, BankAccount
from repository.income_repository import IncomeRepository
from schemas.schemas import IncomeCreate
from .unit_of_work import UnitOfWork


class IncomeService:
    @staticmethod
    def create_income_service(uow: UnitOfWork, income: IncomeCreate) -> Income:
        """Handles business logic for creating a new income."""
        with uow:
            income_repo = uow.incomes  # Get the repository from UnitOfWork

            # Validate bank account existence
            bank_account = uow._session.query(BankAccount).filter(
                BankAccount.name_of_bank == income.name_of_bank
            ).first()

            if not bank_account:
                raise HTTPException(status_code=404, detail="Bank account not found")

            # Prepare Income object
            db_income = Income(
                user_id=bank_account.user_id,
                income_amt=income.income_amt,
                date=income.date,
                description=income.description,
                account_id=bank_account.account_id,
                category_id=income.category_id,
            )

            # Use the repository to create income (no session argument needed)
            created_income = income_repo.create_income(db_income)  # Just pass the income object
            return created_income
        
    @staticmethod
    def get_income_by_id_service(uow: UnitOfWork, income_id: int) -> Income:
        """Handles business logic for fetching income by ID."""
        with uow:
            # Access the repository directly from UnitOfWork
            income_repo = uow.incomes

            # Fetch income using the repository
            income = income_repo.get_income_by_id(income_id)

            if not income:
                raise HTTPException(status_code=404, detail="Income not found")

            return income

    @staticmethod
    def get_all_incomes_service(uow: UnitOfWork):
        """Handles business logic for fetching all incomes."""
        with uow:
            # Access the repository directly from UnitOfWork
            income_repo = uow.incomes

            # Fetch all incomes using the repository
            incomes = income_repo.get_all_incomes()
            return incomes

    @staticmethod
    def update_income_service(uow: UnitOfWork, income_id: int, income: IncomeCreate):
        """Handles business logic for updating an income record."""
        with uow:
            # Access the repository directly from UnitOfWork
            income_repo = uow.incomes

            # Fetch the income record
            db_income = income_repo.get_income_by_id(income_id)

            if not db_income:
                raise HTTPException(status_code=404, detail="Income not found")

            # Fetch bank account for validation
            bank_account = uow._session.query(BankAccount).filter(
                BankAccount.name_of_bank == income.name_of_bank
            ).first()

            if not bank_account:
                raise HTTPException(status_code=404, detail="Bank account not found")

            # Update the fields
            db_income.income_amt = income.income_amt
            db_income.date = income.date
            db_income.description = income.description
            db_income.account_id = bank_account.account_id
            db_income.category_id = income.category_id

            # Use the repository to update the income
            updated_income = income_repo.update_income(db_income)
            return updated_income

    @staticmethod
    def delete_income_service(uow: UnitOfWork, income_id: int):
        """Handles business logic for deleting an income record."""
        with uow:
            # Access the repository directly from UnitOfWork
            income_repo = uow.incomes

            # Use the repository to delete the income
            success = income_repo.delete_income(income_id)

            if not success:
                raise HTTPException(status_code=404, detail="Income not found")

            return {"message": "Income deleted successfully"}
