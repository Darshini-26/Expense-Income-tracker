# utils/expense_utils.py
from models.models import Expense
from sqlalchemy.orm import Session

def create_new_expense(db: Session, amount: float, description: str, date: str, account_id: int, category_id: int) -> Expense:
    """Utility function for creating a new expense."""
    new_expense = Expense(
        expense_amt=amount,
        description=description,
        date=date,
        account_id=account_id,
        category_id=category_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense
