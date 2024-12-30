from sqlalchemy.orm import Session
from models.models import Income

class IncomeRepository:
    @staticmethod
    def create_income(db: Session, income: Income) -> Income:
        db.add(income)
        db.commit()
        db.refresh(income)
        return income

    @staticmethod
    def get_income_by_id(db: Session, income_id: int) -> Income:
        return db.query(Income).filter(Income.income_id == income_id).first()

    @staticmethod
    def get_all_incomes(db: Session):
        return db.query(Income).all()

    @staticmethod
    def update_income(db: Session, income:Income) -> Income:
        db.add(income)
        db.commit()
        db.refresh(income)
        return income
    
    # Delete an income record
    @staticmethod
    def delete_income(db: Session, income_id: int) -> bool:
        db_income = db.query(Income).filter(Income.income_id == income_id).first()
        
        if db_income:
            db.delete(db_income)  # Delete the record
            db.commit()  # Commit the changes to the database
            return {"message": "Record deleted"}
        # return False  # If income with the given ID was not found