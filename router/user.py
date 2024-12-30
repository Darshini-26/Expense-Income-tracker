# router/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.user_service import create_user_service, get_user_by_email_service, get_all_users_service
from config.database import get_db  # Assuming this is your database session

router = APIRouter()

@router.post("/user/")
def create_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    try:
        return create_user_service(db, name, email, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{email}",include_in_schema=False)
def read_user(email: str, db: Session = Depends(get_db)):
    try:
        return get_user_by_email_service(db, email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/users/",include_in_schema=False)
def read_users(db: Session = Depends(get_db)):
    return get_all_users_service(db)
