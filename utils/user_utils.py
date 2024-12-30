# utils/user_utils.py
from models.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_new_user(db: Session, name: str, email: str, password: str) -> User:
    """Utility function for creating a new user."""
    new_user = User(name=name, email=email, password=password)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("Integrity error: User may already exist with the same email.")
    return new_user
