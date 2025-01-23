from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.user_service import create_user_service, get_user_by_email_service, get_all_users_service
from config.database import get_db
from service.unit_of_work import UnitOfWork
from auth.auth import JWTBearer
from schemas.schemas import UserCreate

router = APIRouter()

# Dependency to provide a Unit of Work
def get_uow(db: Session = Depends(get_db)):
    return UnitOfWork(db)

@router.post("/user/",dependencies= [Depends(JWTBearer())])
def create_user(user: UserCreate,  uow: UnitOfWork = Depends(get_uow)):
    try:
        return create_user_service(uow, user.name, user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{email}", include_in_schema=False,dependencies= [Depends(JWTBearer())])
def read_user(email: str, uow: UnitOfWork = Depends(get_uow)):
    try:
        return get_user_by_email_service(uow, email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/users/", include_in_schema=False,dependencies= [Depends(JWTBearer())])
def read_users(uow: UnitOfWork = Depends(get_uow)):
    return get_all_users_service(uow)
