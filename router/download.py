from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from service.download_service import download_incomes_expenses_as_csv  # Import the service function
from service.unit_of_work import UnitOfWork
from sqlalchemy.orm import sessionmaker
from typing import Callable
from sqlalchemy.orm import Session
from config.database import engine  # Assuming engine is set up for database connection

router = APIRouter(tags=['Download'])

# Dependency to get the session factory
def get_session_factory():
    SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionFactory

# Endpoint to download incomes and expenses as CSV
@router.get("/download/csv")
def download_csv(session_factory: Callable[[], Session] = Depends(get_session_factory)):
    with UnitOfWork(session_factory) as uow:
        return download_incomes_expenses_as_csv(uow)

