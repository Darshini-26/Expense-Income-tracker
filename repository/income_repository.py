from sqlalchemy.orm import Session
from models.models import Income

class IncomeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        """
        Fetch all income records from the database.

        Returns:
            list: A list of Income objects.
        """
        return self.session.query(Income).all()

    def create_income(self, income: Income) -> Income:
        """Create a new income record in the database."""
        self.session.add(income)
        self.session.commit()  # Commit the transaction
        self.session.refresh(income)  # Refresh the instance to get the generated ID, etc.
        return income

    def get_income_by_id(self, income_id: int) -> Income:
        """Get an income record by its ID."""
        income = self.session.query(Income).filter(Income.income_id == income_id).first()
        if income:
            # Ensure the income instance is refreshed with the current session
            self.session.refresh(income)
        return income

    def get_all_incomes(self):
        """Get all income records."""
        incomes = self.session.query(Income).all()
        for income in incomes:
            self.session.refresh(income)  # Ensure all incomes are fresh
        return incomes

    def update_income(self, income: Income) -> Income:
        """Update an existing income record."""
        # Attach the income to the session if it's detached
        db_income = self.session.merge(income)
        self.session.commit()  # Commit the transaction
        self.session.refresh(db_income)  # Refresh the instance to get the updated data
        return db_income

    def delete_income(self, income_id: int) -> bool:
        """Delete an income record by its ID."""
        db_income = self.session.query(Income).filter(Income.income_id == income_id).first()
        
        if db_income:
            self.session.delete(db_income)  # Delete the income record
            self.session.commit()  # Commit the transaction to finalize the deletion
            return True
        return False  # Return False if no record with that ID was found
