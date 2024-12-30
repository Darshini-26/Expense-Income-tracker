# utils/income_utils.py
from models.models import Income
from sqlalchemy.orm import Session

def create_new_income(db: Session, amount: float, description: str, date: str, account_id: int, category_id: int) -> Income:
    """Utility function for creating a new income."""
    new_income = Income(
        income_amt=amount,
        description=description,
        date=date,
        account_id=account_id,
        category_id=category_id
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income
