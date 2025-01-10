# service/user_service.py
from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from utils.user_utils import create_new_user
from models.models import User
from .unit_of_work import UnitOfWork

def create_user_service(uow: UnitOfWork,db: Session, name: str, email: str) -> User:
    """Handles business logic for creating a new user."""
    with uow:

    
        existing_user = UserRepository.find_user_by_email(db, email)
        if existing_user:
            raise ValueError("User already exists.")
    
    # Create user using utility function
        user = create_new_user(db, name, email)
        return user

def get_user_by_email_service(uow: UnitOfWork,db: Session, email: str) -> User:
    """Handles business logic for fetching user by email."""
    with uow:
        user = UserRepository.find_user_by_email(db, email)
        if not user:
            raise ValueError("User not found.")
        return user

def get_all_users_service(uow: UnitOfWork,db: Session):
    """Handles business logic for fetching all users."""
    with uow:
        return UserRepository.get_all_users(db)
