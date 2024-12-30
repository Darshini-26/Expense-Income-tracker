from sqlalchemy.orm import Session
from repository.bank_account_repository import BankAccountRepository
from models.models import BankAccount
from fastapi import HTTPException
from schemas.schemas import BankAccountCreate
from models.models import User,BankAccount
from schemas.schemas import BankAccountCreate
from random import randint

class BankAccountService:
    @staticmethod
    def create_bank_account_service(db: Session, bank_account: BankAccountCreate):
        # Step 1: Check if the user exists by email
        user = db.query(User).filter(User.email == bank_account.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User with the provided email does not exist")
        
        # Step 2: Check for duplicate bank names for the user
        existing_bank = (
            db.query(BankAccount)
            .filter(BankAccount.user_id == user.user_id, BankAccount.name_of_bank == bank_account.name_of_bank)
            .first()
        )
        if existing_bank:
            raise HTTPException(status_code=400, detail="Bank name is already associated with this user")
        
        # Step 3: Generate a unique 16-digit account number
        while True:
            account_no = randint(10**15, 10**16 - 1)
            if not db.query(BankAccount).filter(BankAccount.account_no == account_no).first():
                break
        
        # Step 4: Create a new bank account record
        db_account = BankAccount(
            balance=bank_account.balance,
            name_of_bank=bank_account.name_of_bank,
            account_no=account_no,
            user_id=user.user_id
        )
        return BankAccountRepository.create_bank_account(db, db_account)

    @staticmethod
    def get_bank_account_by_id_service(db: Session, account_id: int) -> BankAccount:
        bank_account = BankAccountRepository.get_bank_account_by_id(db, account_id)
        if not bank_account:
            raise ValueError("Bank account not found.")
        return bank_account

    @staticmethod
    def get_all_bank_accounts_service(db: Session):
        return BankAccountRepository.get_all_bank_accounts(db)

    @staticmethod
    def update_bank_account_service(db: Session,account_id: int, bank_account: BankAccountCreate) -> BankAccount:
        db_account = db.query(BankAccount).filter(BankAccount.account_id == account_id).first()
        if not db_account:
            raise HTTPException(status_code=404, detail="Bank account not found")

        db_account.balance = bank_account.balance
        db_account.name_of_bank = bank_account.name_of_bank
        return BankAccountRepository.update_bank_account(db,db_account)

    @staticmethod
    def delete_bank_account_service(db: Session, account_id: int):
        return BankAccountRepository.delete_bank_account(db, account_id)
