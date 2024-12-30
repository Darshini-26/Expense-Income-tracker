# utils/category_utils.py
from models.models import Category
from sqlalchemy.orm import Session

def create_new_category(db: Session, category_type: str) -> Category:
    """Utility function for creating a new category."""
    new_category = Category(category_type=category_type)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
