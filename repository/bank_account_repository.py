from sqlalchemy.orm import Session
from models.models import BankAccount

class BankAccountRepository:
    @staticmethod
    def create_bank_account(db: Session, bank_account: BankAccount) -> BankAccount:
        db.add(bank_account)
        db.commit()
        db.refresh(bank_account)
        return bank_account

    @staticmethod
    def get_bank_account_by_id(db: Session, account_id: int) -> BankAccount:
        return db.query(BankAccount).filter(BankAccount.account_id == account_id).first()

    @staticmethod
    def get_all_bank_accounts(db: Session):
        return db.query(BankAccount).all()

    @staticmethod
    def update_bank_account(db: Session, bank_account: BankAccount) -> BankAccount:
        db.add(bank_account)
        db.commit()
        db.refresh(bank_account)
        return bank_account

    @staticmethod
    def delete_bank_account(db: Session, account_id: int) -> dict:
        db_bank_account = db.query(BankAccount).filter(BankAccount.account_id == account_id).first()
        if db_bank_account:
            db.delete(db_bank_account)
            db.commit()
            return {"message": "Bank account deleted"}
        return {"message": "Bank account not found"}
