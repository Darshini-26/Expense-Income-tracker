from sqlalchemy.orm import Session
from models.models import Expense

class ExpenseRepository:
    @staticmethod
    def create_expense(db: Session, expense: Expense) -> Expense:
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def get_expense_by_id(db: Session, expense_id: int) -> Expense:
        return db.query(Expense).filter(Expense.expense_id == expense_id).first()

    @staticmethod
    def get_all_expenses(db: Session):
        return db.query(Expense).all()

    @staticmethod
    def update_expense(db: Session, expense: Expense) -> Expense:
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense
    
    # Delete an expense record
    @staticmethod
    def delete_expense(db: Session, expense_id: int) -> dict:
        db_expense = db.query(Expense).filter(Expense.expense_id == expense_id).first()
        
        if db_expense:
            db.delete(db_expense)  # Delete the record
            db.commit()  # Commit the changes to the database
            return {"message": "Record deleted"}
        else:
            return {"message": "Expense not found"}
