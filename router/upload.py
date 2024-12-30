from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from models import models
import pandas as pd
from repository.s3_repository import upload_to_s3
from models.models import Income, Expense, BankAccount, Category

# Define your S3 bucket name
BUCKET_NAME = "financial-tracker1"

router = APIRouter(tags=["Upload"])

@router.get("/income/upload")
def upload_income_data_to_s3(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Upload income data to S3.
    """
    try:
        # Fetch income data as a DataFrame
        incomes_df = pd.read_sql(db.query(models.Income).statement, db.bind)
        
        # Generate a temporary file name for the CSV
        file_name = "incomes.csv"
        
        # Save the DataFrame to a CSV file locally
        incomes_df.to_csv(file_name, index=False)

        # Upload the CSV file to S3
        file_url = upload_to_s3(file_name, BUCKET_NAME)

        # Optionally delete the local file after uploading
        import os
        os.remove(file_name)

        # Return the S3 file URL in the response
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    
    except Exception as e:
        # Handle any exceptions and return an appropriate error message
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/expense/upload")
def upload_expense_data_to_s3(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Uploads expense data as a CSV file to an S3 bucket.

    Args:
        db (Session): Database session injected via dependency.

    Returns:
        JSONResponse: A response with the upload status and file URL.
    """
    expenses_df = pd.read_sql(db.query(models.Expense).statement, db.bind)
    file_name = "expenses.csv"
    expenses_df.to_csv(file_name, index=False)

    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bank_accounts/upload")
def upload_bank_accounts_to_s3(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Uploads all bank accounts to S3 in a CSV format.

    Args:
        db (Session, optional): The database session.

    Returns:
        JSONResponse: A message with the result of the upload.
    """
    # Query the database for bank accounts
    bank_accounts = db.query(models.BankAccount).all()
    
    # Convert the SQLAlchemy query results into a Pandas DataFrame
    bank_accounts_df = pd.DataFrame([{
        "account_id": account.account_id,
        "name_of_bank": account.name_of_bank,
        "balance": account.balance
    } for account in bank_accounts])
    
    # Define the CSV file name
    file_name = "bank_accounts.csv"
    
    # Write the DataFrame to a CSV file
    bank_accounts_df.to_csv(file_name, index=False)
    
    # Upload the CSV file to S3
    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/upload")
def upload_category_to_s3(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Uploads all categories to S3 in CSV format.

    Args:
        db (Session, optional): The database session.

    Returns:
        JSONResponse: A message with the result of the upload.
    """
    # Query the database for categories and load the result directly into a Pandas DataFrame
    categories_df = pd.read_sql(db.query(models.Category).statement, db.bind)

    # Define the CSV file name
    file_name = "categories.csv"

    # Write the DataFrame to a CSV file
    categories_df.to_csv(file_name, index=False, columns=["category_id", "category_type"])

    # Upload the CSV file to S3
    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

