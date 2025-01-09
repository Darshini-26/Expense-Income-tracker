from fastapi import HTTPException
from models.models import Expense, BankAccount
from repository.expense_repository import ExpenseRepository
from schemas.schemas import ExpenseCreate
from .unit_of_work import UnitOfWork


class ExpenseService:
    @staticmethod
    def create_expense_service(uow: UnitOfWork, expense: ExpenseCreate) -> Expense:
        """Handles business logic for creating a new expense."""
        with uow:
            expense_repo = uow.expenses  # Get the repository from UnitOfWork

            # Validate bank account existence
            bank_account = uow._session.query(BankAccount).filter(
                BankAccount.name_of_bank == expense.name_of_bank
            ).first()

            if not bank_account:
                raise HTTPException(status_code=404, detail="Bank account not found")

            # Prepare Expense object
            db_expense = Expense(
                user_id=bank_account.user_id,
                expense_amt=expense.expense_amt,
                date=expense.date,
                description=expense.description,
                account_id=bank_account.account_id,
                category_id=expense.category_id,
            )

            # Use the repository to create expense (no session argument needed)
            created_expense = expense_repo.create_expense(db_expense)
 # Just pass the expense object
            return created_expense

    @staticmethod
    def get_expense_by_id_service(uow: UnitOfWork, expense_id: int) -> Expense:
        """Handles business logic for fetching expense by ID."""
        with uow:
            # Access the repository directly from UnitOfWork
            expense_repo = uow.expenses

            # Fetch expense using the repository
            expense = expense_repo.get_expense_by_id(expense_id)

            if not expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            return expense

    @staticmethod
    def get_all_expenses_service(uow: UnitOfWork):
        """Handles business logic for fetching all expenses."""
        with uow:
            # Access the repository directly from UnitOfWork
            expense_repo = uow.expenses

            # Fetch all expenses using the repository
            expenses = expense_repo.get_all_expenses()
            return expenses

    @staticmethod
    def update_expense_service(uow: UnitOfWork, expense_id: int, expense: ExpenseCreate):
        """Handles business logic for updating an expense record."""
        with uow:
            # Access the repository directly from UnitOfWork
            expense_repo = uow.expenses

            # Fetch the expense record
            db_expense = expense_repo.get_expense_by_id(expense_id)

            if not db_expense:
                raise HTTPException(status_code=404, detail="Expense not found")

            # Fetch bank account for validation
            bank_account = uow._session.query(BankAccount).filter(
                BankAccount.name_of_bank == expense.name_of_bank
            ).first()

            if not bank_account:
                raise HTTPException(status_code=404, detail="Bank account not found")

            # Update the fields
            db_expense.expense_amt = expense.expense_amt
            db_expense.date = expense.date
            db_expense.description = expense.description
            db_expense.account_id = bank_account.account_id
            db_expense.category_id = expense.category_id

            # Use the repository to update the expense
            updated_expense = expense_repo.update_expense(db_expense)
            return updated_expense

    @staticmethod
    def delete_expense_service(uow: UnitOfWork, expense_id: int):
        """Handles business logic for deleting an expense record."""
        with uow:
            # Access the repository directly from UnitOfWork
            expense_repo = uow.expenses

            # Use the repository to delete the expense
            success = expense_repo.delete_expense(expense_id)

            if not success:
                raise HTTPException(status_code=404, detail="Expense not found")

            return {"message": "Expense deleted successfully"}
