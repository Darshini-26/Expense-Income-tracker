# service/expense_service.py
from sqlalchemy.orm import Session
from repository.expense_repository import ExpenseRepository
from utils.expense_utils import create_new_expense
from models.models import Expense, BankAccount
from fastapi import HTTPException
from schemas.schemas import ExpenseCreate

class ExpenseService:
    @staticmethod
    def create_expense_service(db: Session, expense: ExpenseCreate) -> Expense:
        """Handles business logic for creating a new expense."""
        bank_account = db.query(BankAccount).filter(
            BankAccount.name_of_bank == expense.name_of_bank
        ).first()
        if not bank_account:
            raise HTTPException(status_code=404, detail="Bank account not found")
        db_expense = Expense(
            user_id=bank_account.user_id,
            expense_amt=expense.expense_amt,
            date=expense.date,
            description=expense.description,
            account_id=bank_account.account_id,
            category_id=expense.category_id,
        )
        return ExpenseRepository.create_expense(db, db_expense)

    @staticmethod
    def get_expense_by_id_service(db: Session, expense_id: int) -> Expense:
        """Handles business logic for fetching expense by ID."""
        expense = ExpenseRepository.get_expense_by_id(db, expense_id)
        if not expense:
            raise ValueError("Expense not found.")
        return expense

    @staticmethod
    def get_all_expenses_service(db: Session):
        """Handles business logic for fetching all expenses."""
        return ExpenseRepository.get_all_expenses(db)

    @staticmethod
    def update_expense_service(db: Session, expense_id: int, expense: ExpenseCreate):
        db_expense = db.query(Expense).filter(Expense.expense_id == expense_id).first()
        if not db_expense:
            raise HTTPException(status_code=404, detail="Expense not found")

        bank_account = db.query(BankAccount).filter(
            BankAccount.name_of_bank == expense.name_of_bank
        ).first()
        if not bank_account:
            raise HTTPException(status_code=404, detail="Bank account not found")

        db_expense.expense_amt = expense.expense_amt
        db_expense.date = expense.date
        db_expense.description = expense.description
        db_expense.account_id = bank_account.account_id
        db_expense.category_id = expense.category_id

        return ExpenseRepository.update_expense(db, db_expense)

    @staticmethod
    def delete_expense_service(db: Session, expense_id: int):
        return ExpenseRepository.delete_expense(db, expense_id)
