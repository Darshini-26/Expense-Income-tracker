from sqlalchemy.orm import Session
from models.models import User

class UserRepository:
    @staticmethod
    def add_user(uow, db: Session, user: User) -> User:
        """Add a new user to the database."""
        with uow:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    @staticmethod
    def find_user_by_email(uow, db: Session, email: str) -> User:
        """Find a user by email."""
        with uow:
            return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(uow, db: Session):
        """Fetch all users from the database."""
        with uow:
            return db.query(User).all()
