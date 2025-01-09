from sqlalchemy.orm import Session
from models.models import Expense

class ExpenseRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        """
        Fetch all income records from the database.

        Returns:
            list: A list of Income objects.
        """
        return self.session.query(Expense).all()

    def create_expense(self, expense: Expense) -> Expense:
        self.session.add(expense)  # Use self.session instead of requiring db as an argument
        self.session.commit()
        self.session.refresh(expense)
        return expense


    def get_expense_by_id(self, expense_id: int) -> Expense:
        """Get an expense record by its ID."""
        expense = self.session.query(Expense).filter(Expense.expense_id == expense_id).first()
        if expense:
            # Ensure the expense instance is refreshed with the current session
            self.session.refresh(expense)
        return expense

    def get_all_expenses(self):
        """Get all expense records."""
        expenses = self.session.query(Expense).all()
        for expense in expenses:
            self.session.refresh(expense)  # Ensure all expenses are fresh
        return expenses

    def update_expense(self, expense: Expense) -> Expense:
        """Update an existing expense record."""
        db_expense = self.session.merge(expense)  # Merge the updated expense into the session
        self.session.commit()  # Commit the transaction
        self.session.refresh(db_expense)  # Refresh the instance to get the updated data
        return db_expense

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense record by its ID."""
        db_expense = self.session.query(Expense).filter(Expense.expense_id == expense_id).first()
        
        if db_expense:
            self.session.delete(db_expense)  # Delete the expense record
            self.session.commit()  # Commit the transaction to finalize the deletion
            return True
        return False  # Return False if no record with that ID was found
