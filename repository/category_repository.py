from sqlalchemy.orm import Session
from models.models import Category

class CategoryRepository:
    @staticmethod
    def create_category(db: Session, category: Category) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Category:
        return db.query(Category).filter(Category.category_id == category_id).first()

    @staticmethod
    def get_all_categories(db: Session):
        return db.query(Category).all()

    @staticmethod
    def update_category(db: Session, category: Category) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        
        if db_category:
            db.delete(db_category)  # Delete the record
            db.commit()  # Commit the changes to the database
            return {"message": "Category deleted successfully"}
        return False  # If category with the given ID was not found
