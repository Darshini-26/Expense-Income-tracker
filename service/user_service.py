# service/user_service.py
from sqlalchemy.orm import Session
from repository.user_repository import add_user, find_user_by_email, get_all_users
from utils.user_utils import create_new_user
from models.models import User

def create_user_service(db: Session, name: str, email: str, password: str) -> User:
    """Handles business logic for creating a new user."""
    if not name or not email or not password:
        raise ValueError("All fields must be provided.")
    
    existing_user = find_user_by_email(db, email)
    if existing_user:
        raise ValueError("User already exists.")
    
    # Create user using utility function
    user = create_new_user(db, name, email, password)
    return user

def get_user_by_email_service(db: Session, email: str) -> User:
    """Handles business logic for fetching user by email."""
    user = find_user_by_email(db, email)
    if not user:
        raise ValueError("User not found.")
    return user

def get_all_users_service(db: Session):
    """Handles business logic for fetching all users."""
    return get_all_users(db)
