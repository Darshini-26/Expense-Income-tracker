from fastapi import FastAPI, HTTPException, status, Depends
from typing import List, Generator
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import uuid

from src.database import SessionLocal, engine
import src.models as models
import src.schemas as schemas

# Initialize database and app
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

BUCKET_NAME = "financial-tracker1"

# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root() -> dict:
    """
    Root endpoint to check the application status.
    """
    return {"message": "FastAPI with SSM integration is working!"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)) -> dict:
    """
    Simple endpoint to test database connection.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    """
    Create a new user.
    """
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        user_id=str(uuid.uuid4()),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/income/", tags=["INCOME"], response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)) -> schemas.Income:
    """
    Create a new income entry.
    """
    bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == income.name_of_bank
    ).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db_income = models.Income(
        user_id=bank_account.user_id,
        income_amt=income.income_amt,
        date=income.date,
        description=income.description,
        account_id=bank_account.account_id,
        category_id=income.category_id,
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

@app.get("/income/upload", tags=["INCOME"])
def upload_income_data_to_s3(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Upload income data to S3.
    """
    incomes_df = pd.read_sql(db.query(models.Income).statement, db.bind)
    file_name = "incomes.csv"
    incomes_df.to_csv(file_name, index=False)

    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/income/", tags=["INCOME"], response_model=List[schemas.Income])
def read_income(db: Session = Depends(get_db)) -> List[schemas.Income]:
    """
    Fetch all income records.
    """
    return db.query(models.Income).all()

@app.get("/income/{name_of_bank}", tags=["INCOME"], response_model=List[schemas.Income])
def read_income_by_bank(name_of_bank: str, db: Session = Depends(get_db)) -> List[schemas.Income]:
    """
    Fetch all income records by bank name.
    """
    bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == name_of_bank
    ).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    incomes = db.query(models.Income).filter(
        models.Income.account_id == bank_account.account_id
    ).all()
    if not incomes:
        raise HTTPException(status_code=404, detail="No incomes found for this bank")
    return incomes

@app.put("/income/{income_id}", tags=["INCOME"], response_model=schemas.Income)
def update_income(
    income_id: int, income: schemas.IncomeCreate, db: Session = Depends(get_db)
) -> schemas.Income:
    """
    Update an income record.
    """
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")

    bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == income.name_of_bank
    ).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db_income.income_amt = income.income_amt
    db_income.date = income.date
    db_income.description = income.description
    db_income.account_id = bank_account.account_id
    db_income.category_id = income.category_id

    db.commit()
    db.refresh(db_income)
    return db_income

@app.delete("/income/{income_id}", tags=["INCOME"])
def delete_income(income_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete an income record.
    """
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    
    db.delete(db_income)
    db.commit()
    return {"message": "Record deleted"}


# EXPENSE Routes
@app.post("/expense/", tags=["EXPENSE"], response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)) -> schemas.Expense:
    """
    Creates a new expense record.

    Args:
        expense (schemas.ExpenseCreate): Expense details provided in the request body.
        db (Session): Database session injected via dependency.

    Returns:
        schemas.Expense: The created expense record.
    """
    bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == expense.name_of_bank
    ).first()

    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db_expense = models.Expense(
        user_id=bank_account.user_id,
        expense_amt=expense.expense_amt,
        date=expense.date,
        description=expense.description,
        account_id=bank_account.account_id,
        category_id=expense.category_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expense/upload", tags=["EXPENSE"])
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


@app.get("/expense/", tags=["EXPENSE"], response_model=List[schemas.Expense])
def read_expense(db: Session = Depends(get_db)) -> List[schemas.Expense]:
    """
    Retrieves all expense records.

    Args:
        db (Session): Database session injected via dependency.

    Returns:
        List[schemas.Expense]: A list of all expense records.
    """
    return db.query(models.Expense).all()


@app.get("/expense/{name_of_bank}", tags=["EXPENSE"], response_model=List[schemas.Expense])
def read_expense_by_bank(name_of_bank: str, db: Session = Depends(get_db)) -> List[schemas.Expense]:
    """
    Retrieves expense records for a specific bank.

    Args:
        name_of_bank (str): The name of the bank.
        db (Session): Database session injected via dependency.

    Returns:
        List[schemas.Expense]: A list of expense records associated with the bank.
    """
    bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == name_of_bank
    ).first()

    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    expenses = db.query(models.Expense).filter(
        models.Expense.account_id == bank_account.account_id
    ).all()

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this bank")

    return expenses


@app.put("/expense/{expense_id}", tags=["EXPENSE"], response_model=schemas.Expense)
def update_expense(
    expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)
) -> schemas.Expense:
    """
    Updates an existing expense record.

    Args:
        expense_id (int): ID of the expense to update.
        expense (schemas.ExpenseCreate): Updated expense details.
        db (Session): Database session injected via dependency.

    Returns:
        schemas.Expense: The updated expense record.
    """
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    bank_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == expense.name_of_bank
    ).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db_expense.expense_amt = expense.expense_amt
    db_expense.date = expense.date
    db_expense.description = expense.description
    db_expense.account_id = bank_account.account_id
    db_expense.category_id = expense.category_id

    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expense/{expense_id}", tags=["EXPENSE"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Deletes an expense record by ID.

    Args:
        expense_id (int): ID of the expense to delete.
        db (Session): Database session injected via dependency.

    Returns:
        dict: A confirmation message.
    """
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"message": "Record deleted"}


# Helper Function
def clean_up_account_numbers(db: Session) -> None:
    """
    Ensures all bank accounts have valid numeric account numbers.
    Generates a unique 16-digit account number for accounts with missing values.

    Args:
        db (Session): Database session injected via dependency.
    """
    invalid_accounts = db.query(models.BankAccount).filter(models.BankAccount.account_no == None).all()

    for account in invalid_accounts:
        while True:
            new_account_no = randint(10**15, 10**16 - 1)
            if not db.query(models.BankAccount).filter(models.BankAccount.account_no == new_account_no).first():
                account.account_no = new_account_no
                break
        db.commit()

@app.post("/bank_account/", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def create_bank_account(
    bank_account: schemas.BankAccountCreate, db: Session = Depends(get_db)
) -> schemas.BankAccount:
    """
    Creates a new bank account for a user.

    Args:
        bank_account (schemas.BankAccountCreate): The bank account details to create.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the user does not exist or the bank name is already associated.

    Returns:
        schemas.BankAccount: The created bank account.
    """
    user = db.query(models.User).filter(models.User.email == bank_account.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with the provided email does not exist")
    
    # Check if the bank name is already associated with this user
    existing_bank = (
        db.query(models.BankAccount)
        .filter(models.BankAccount.user_id == user.user_id, models.BankAccount.name_of_bank == bank_account.name_of_bank)
        .first()
    )
    if existing_bank:
        raise HTTPException(status_code=400, detail="Bank name is already associated with this user")
    
    # Generate a unique account number
    while True:
        account_no = randint(10**15, 10**16 - 1)  # Generate 16-digit number
        if not db.query(models.BankAccount).filter(models.BankAccount.account_no == account_no).first():
            break

    db_account = models.BankAccount(
        balance=bank_account.balance,
        name_of_bank=bank_account.name_of_bank,
        account_no=account_no,
        user_id=user.user_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@app.get("/bank_account/", tags=["BANK ACCOUNT"], response_model=List[schemas.BankAccount])
def read_bank_account(db: Session = Depends(get_db)) -> List[schemas.BankAccount]:
    """
    Retrieves all bank accounts.

    Args:
        db (Session, optional): The database session.

    Returns:
        List[schemas.BankAccount]: A list of bank accounts.
    """
    db_account = db.query(models.BankAccount).all()
    return db_account


@app.get("/bank_accounts/upload", tags=["BANK ACCOUNT"])
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


@app.get("/bank_account/{name_of_bank}", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def read_bank_account_by_name(
    name_of_bank: str, db: Session = Depends(get_db)
) -> schemas.BankAccount:
    """
    Retrieves a bank account by its bank name.

    Args:
        name_of_bank (str): The name of the bank.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If no bank account with the given name exists.

    Returns:
        schemas.BankAccount: The bank account associated with the given bank name.
    """
    # Query the bank account by name
    db_account = db.query(models.BankAccount).filter(
        models.BankAccount.name_of_bank == name_of_bank
    ).first()
    
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    return db_account


@app.put("/bank_account/{account_id}", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def update_bank_account(
    account_id: int, bank_account: schemas.BankAccountCreate, db: Session = Depends(get_db)
) -> schemas.BankAccount:
    """
    Updates a bank account's details.

    Args:
        account_id (int): The ID of the bank account to update.
        bank_account (schemas.BankAccountCreate): The updated bank account details.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the bank account with the given ID does not exist.

    Returns:
        schemas.BankAccount: The updated bank account.
    """
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    db_account.balance = bank_account.balance
    db_account.name_of_bank = bank_account.name_of_bank
    db.commit()
    db.refresh(db_account)
    return db_account


@app.delete("/bank_account/{account_id}", tags=["BANK ACCOUNT"])
def delete_bank_account(account_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Deletes a bank account by its ID.

    Args:
        account_id (int): The ID of the bank account to delete.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the bank account with the given ID does not exist.

    Returns:
        dict: A message indicating that the bank account was deleted.
    """
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    db.delete(db_account)
    db.commit()
    return {"Message": "Records deleted"}

@app.post("/categories/", tags=["CATEGORY"], response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(get_db)
) -> schemas.Category:
    """
    Creates a new category.

    Args:
        category (schemas.CategoryCreate): The category details to create.
        db (Session, optional): The database session.

    Returns:
        schemas.Category: The created category.
    """
    if category.category_type == "Income":
        category_id = 1
    elif category.category_type == "Expense":
        category_id = 2
    else:
        raise HTTPException(status_code=400, detail="Invalid category type")

    db_category = models.Category(
        category_type=category.category_type, category_id=category_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories/upload", tags=["CATEGORY"])
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


@app.get("/categories/", tags=["CATEGORY"], response_model=List[schemas.Category])
def read_category(db: Session = Depends(get_db)) -> List[schemas.Category]:
    """
    Retrieves all categories.

    Args:
        db (Session, optional): The database session.

    Returns:
        List[schemas.Category]: A list of categories.
    """
    db_category = db.query(models.Category).all()
    return db_category


@app.get("/categories/{category_id}", tags=["CATEGORY"], response_model=schemas.Category)
def read_category_by_id(
    category_id: int, db: Session = Depends(get_db)
) -> schemas.Category:
    """
    Retrieves a category by its ID.

    Args:
        category_id (int): The ID of the category to retrieve.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the category ID is invalid or not found.

    Returns:
        schemas.Category: The category associated with the given ID.
    """
    if category_id not in [1, 2]:  # Validating that only 1 or 2 can exist
        raise HTTPException(status_code=404, detail="Category not found")

    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    return db_category


@app.put("/categories/{category_id}", tags=["CATEGORY"], response_model=schemas.Category)
def update_category(
    category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)
) -> schemas.Category:
    """
    Updates a category's details.

    Args:
        category_id (int): The ID of the category to update.
        category (schemas.CategoryCreate): The updated category details.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the category with the given ID does not exist.

    Returns:
        schemas.Category: The updated category.
    """
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.category_type = category.category_type
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}", tags=["CATEGORY"])
def delete_category(category_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Deletes a category by its ID.

    Args:
        category_id (int): The ID of the category to delete.
        db (Session, optional): The database session.

    Raises:
        HTTPException: If the category with the given ID does not exist.

    Returns:
        dict: A message indicating that the category was deleted.
    """
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return {"Message": "Records deleted"}


def upload_to_s3(file_name: str, bucket_name: str, object_name: str = None) -> str:
    """
    Uploads a file to an S3 bucket.

    Args:
        file_name (str): The file to upload.
        bucket_name (str): The S3 bucket name.
        object_name (str, optional): The name of the object in the S3 bucket. Defaults to None.

    Returns:
        str: The URL of the uploaded file.

    Raises:
        Exception: If the file is not found or credentials are unavailable.
    """
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = file_name
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except FileNotFoundError:
        raise Exception("The file was not found")
    except NoCredentialsError:
        raise Exception("Credentials not available")


@app.get("/download-data", response_class=StreamingResponse)
def download_data(db: Session = Depends(get_db)) -> StreamingResponse:
    """
    Endpoint to download income and expense data as a CSV file using pandas.

    Args:
        db (Session, optional): The database session.

    Returns:
        StreamingResponse: A CSV file of income and expense data.
    """
    # Query the database for income and expense data
    incomes = db.query(models.Income).all()
    expenses = db.query(models.Expense).all()

    # Directly convert SQLAlchemy query result into a pandas DataFrame
    income_df = pd.read_sql(db.query(models.Income).statement, db.bind)
    expense_df = pd.read_sql(db.query(models.Expense).statement, db.bind)

    # Add "Type" column to differentiate income and expense rows
    income_df['Type'] = 'Income'
    expense_df['Type'] = 'Expense'

    # Reorder columns to match the required CSV format
    income_df = income_df[['Type', 'income_amt', 'date', 'description', 'account_id', 'category_id']]
    expense_df = expense_df[['Type', 'expense_amt', 'date', 'description', 'account_id', 'category_id']]

    # Rename columns to match the CSV headers
    income_df.columns = ['Type', 'Amount', 'Date', 'Description', 'Account ID', 'Category ID']
    expense_df.columns = ['Type', 'Amount', 'Date', 'Description', 'Account ID', 'Category ID']

    # Concatenate both DataFrames
    all_data_df = pd.concat([income_df, expense_df], ignore_index=True)

    # Create an in-memory file for CSV data
    output = io.StringIO()

    # Write the DataFrame to the in-memory file as CSV
    all_data_df.to_csv(output, index=False)

    # Reset file pointer to the beginning
    output.seek(0)

    # Return the CSV as a streaming response
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"},
    )