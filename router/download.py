from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.file_service import  download_data_as_csv
from config.database import get_db

router = APIRouter(tags=["File"])

@router.get("/download_csv/")
def download_data_as_csv_route(db: Session = Depends(get_db)):
    """
    Downloads income and expense data as a CSV file.
    """
    try:
        return download_data_as_csv(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))