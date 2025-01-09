from sqlalchemy.orm import Session
from repository.bank_account_repository import BankAccountRepository
from models.models import BankAccount, User
from fastapi import HTTPException
from schemas.schemas import BankAccountCreate
from random import randint
from .unit_of_work import UnitOfWork

class BankAccountService:
    @staticmethod
    def create_bank_account_service(uow: UnitOfWork, bank_account: BankAccountCreate) -> BankAccount:
        """Create a new bank account."""
        with uow:
            user = uow._session.query(User).filter(User.email == bank_account.email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User with the provided email does not exist")
            
            # Check for duplicate bank names for the user
            existing_bank = (
                uow._session.query(BankAccount)
                .filter(BankAccount.user_id == user.user_id, BankAccount.name_of_bank == bank_account.name_of_bank)
                .first()
            )
            if existing_bank:
                raise HTTPException(status_code=400, detail="Bank name is already associated with this user")
            
            # Generate a unique 16-digit account number
            while True:
                account_no = randint(10**15, 10**16 - 1)
                if not uow._session.query(BankAccount).filter(BankAccount.account_no == account_no).first():
                    break
            
            # Create a new bank account record
            db_account = BankAccount(
                balance=bank_account.balance,
                name_of_bank=bank_account.name_of_bank,
                account_no=account_no,
                user_id=user.user_id
            )
            created_account = uow.bank_accounts.create_bank_account(db_account)
            uow.commit()
            return created_account

    @staticmethod
    def get_bank_account_by_id_service(uow: UnitOfWork, account_id: int) -> BankAccount:
        """Fetch a bank account by ID."""
        with uow:
            bank_account = uow.bank_accounts.get_bank_account_by_id(account_id)
            if not bank_account:
                raise HTTPException(status_code=404, detail="Bank account not found")
            return bank_account

    @staticmethod
    def get_all_bank_accounts_service(uow: UnitOfWork):
        """Fetch all bank accounts."""
        with uow:
            return uow.bank_accounts.get_all_bank_accounts()

    @staticmethod
    def update_bank_account_service(uow: UnitOfWork, account_id: int, bank_account: BankAccountCreate) -> BankAccount:
        """Update a bank account."""
        with uow:
            db_account = uow._session.query(BankAccount).filter(BankAccount.account_id == account_id).first()
            if not db_account:
                raise HTTPException(status_code=404, detail="Bank account not found")

            # Update fields
            db_account.balance = bank_account.balance
            db_account.name_of_bank = bank_account.name_of_bank

            updated_account = uow.bank_accounts.update_bank_account(db_account)
            uow.commit()
            return updated_account

    @staticmethod
    def delete_bank_account_service(uow: UnitOfWork, account_id: int):
        """Delete a bank account by ID."""
        with uow:
            success = uow.bank_accounts.delete_bank_account(account_id)
            if not success:
                raise HTTPException(status_code=404, detail="Bank account not found")
            uow.commit()
            return {"message": "Bank account deleted successfully"}
