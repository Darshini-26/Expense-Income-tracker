# utils/bank_account_utils.py
from models.models import BankAccount
from sqlalchemy.orm import Session

def create_new_bank_account(db: Session, account_name: str, bank_name: str) -> BankAccount:
    """Utility function for creating a new bank account."""
    new_bank_account = BankAccount(account_name=account_name, bank_name=bank_name)
    db.add(new_bank_account)
    db.commit()
    db.refresh(new_bank_account)
    return new_bank_account
