from sqlalchemy.orm import Session
from models.models import BankAccount

class BankAccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_bank_account(self, bank_account: BankAccount) -> BankAccount:
        """Creates a new bank account in the database."""
        self.session.add(bank_account)
        self.session.commit()  # Commit the transaction to save the bank account
        self.session.refresh(bank_account)  # Refresh to get the generated ID, etc.
        return bank_account

    def get_bank_account_by_id(self, account_id: int) -> BankAccount:
        """Fetches a bank account by its ID."""
        return self.session.query(BankAccount).filter(BankAccount.account_id == account_id).first()

    def get_all_bank_accounts(self):
        """Fetches all bank accounts."""
        return self.session.query(BankAccount).all()

    def update_bank_account(self, bank_account: BankAccount) -> BankAccount:
        """Updates an existing bank account."""
        self.session.merge(bank_account)  # Merge the updated bank account into the session
        self.session.commit()  # Commit the transaction to save changes
        self.session.refresh(bank_account)  # Refresh to get the updated data
        return bank_account

    def delete_bank_account(self, account_id: int) -> bool:
        """Deletes a bank account by its ID."""
        db_bank_account = self.session.query(BankAccount).filter(BankAccount.account_id == account_id).first()
        if db_bank_account:
            self.session.delete(db_bank_account)  # Delete from the session
            self.session.commit()  # Commit the transaction to finalize deletion
            return True
        return False
