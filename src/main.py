from fastapi import FastAPI, HTTPException, status
from typing import List
from fastapi import Depends
from src.database import SessionLocal, engine
import src.models as models
import src.schemas as schemas
from sqlalchemy.orm import Session
from random import randint
import uuid
import csv
from fastapi.responses import JSONResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        user_id=str(uuid.uuid4()),  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


'''@app.post("/income/", tags=["INCOME"], response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db) ):
    db_income = models.Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income'''

@app.post("/income/", tags=["INCOME"], response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    # Fetch user_id based on email or another unique field
    user = db.query(models.User).filter(models.User.email == income.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_income = models.Income(
        user_id=user.user_id,  # Associate the user_id
        income_amt=income.income_amt,
        date=income.date,
        description=income.description,
        account_id=income.account_id,
        category_id=income.category_id,
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

import csv
from fastapi.responses import JSONResponse

BUCKET_NAME = "financial-tracker1"

@app.get("/income/upload", tags=["INCOME"])
def upload_income_data_to_s3(db: Session = Depends(get_db)):
    incomes = db.query(models.Income).all()
    file_name = "incomes.csv"
    
    # Write data to CSV file
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["income_id", "income_amt", "date", "description", "account_id", "category_id"])
        for income in incomes:
            writer.writerow([
                income.income_id,
                #income.user_id,
                income.income_amt,
                income.date,
                income.description,
                income.account_id,
                income.category_id,
            ])
    
    # Upload to S3
    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


'''@app.get("/income/", tags=["INCOME"], response_model=List[schemas.Income])
def read_income(db: Session = Depends(get_db)):
    db_income = db.query(models.Income).all()
    return db_income'''


@app.get("/income/{income_id}", tags=["INCOME"], response_model=schemas.Income)
def read_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income


@app.put("/income/{income_id}", tags=["INCOME"], response_model=schemas.Income)
def update_income(income_id: int, income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    db_income.income_amt = income.income_amt
    db_income.description = income.description
    db_income.account_id = income.account_id
    db_income.category_id = income.category_id
    db.commit()
    db.refresh(db_income)
    return db_income


@app.delete("/income/{income_id}", tags=["INCOME"])
def delete_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(models.Income).filter(models.Income.income_id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    db.delete(db_income)
    db.commit()
    return {"Message": "Records deleted"}


# EXPENSE
'''@app.post("/expense/", tags=["EXPENSE"], response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense'''

@app.post("/expense/", tags=["EXPENSE"], response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    # Fetch user_id based on email or another unique field
    user = db.query(models.User).filter(models.User.email == expense.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create an expense object and associate it with the user
    db_expense = models.Expense(
        user_id=user.user_id,  # Associate the user_id with the expense
        expense_amt=expense.expense_amt,
        date=expense.date,
        description=expense.description,
        account_id=expense.account_id,
        category_id=expense.category_id,
    )
    
    # Add the expense to the database and commit the transaction
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)  # Refresh the object to reflect the database state

    return db_expense

@app.get("/expense/upload", tags=["EXPENSE"])
def upload_expense_data_to_s3(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    file_name = "expenses.csv"
    
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["expense_id",  "expense_amt", "date", "description", "account_id", "category_id"])
        for expense in expenses:
            writer.writerow([
                expense.expense_id,
                #expense.user_id,
                expense.expense_amt,
                expense.date,
                expense.description,
                expense.account_id,
                expense.category_id,
            ])
    
    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



'''@app.get("/expense/", tags=["EXPENSE"], response_model=List[schemas.Expense])
def read_expense(db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).all()
    return db_expense'''


@app.get("/expense/{expense_id}", tags=["EXPENSE"], response_model=schemas.Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@app.put("/expense/{expense_id}", tags=["EXPENSE"], response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.expense_amt = expense.expense_amt
    db_expense.description = expense.description
    db_expense.account_id = expense.account_id
    db_expense.category_id = expense.category_id
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expense/{expense_id}", tags=["EXPENSE"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"Message": "Records deleted"}

def clean_up_account_numbers(db: Session):
    # Query rows with non-numeric account_no values
    invalid_accounts = db.query(models.BankAccount).filter(models.BankAccount.account_no == None).all()

    for account in invalid_accounts:
        while True:
            # Generate a new unique 16-digit account number
            new_account_no = randint(10**15, 10**16 - 1)
            if not db.query(models.BankAccount).filter(models.BankAccount.account_no == new_account_no).first():
                account.account_no = new_account_no
                break

        # Commit the changes to the database
        db.commit()

# BANK ACCOUNT
@app.post("/bank_account/", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def create_bank_account(bank_account: schemas.BankAccountCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == bank_account.email).first()
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


'''@app.get("/bank_account/", tags=["BANK ACCOUNT"], response_model=List[schemas.BankAccount])
def read_bank_account(db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).all()
    return db_account'''

@app.get("/bank_accounts/upload", tags=["BANK ACCOUNT"])
def upload_bank_accounts_to_s3(db: Session = Depends(get_db)):
    bank_accounts = db.query(models.BankAccount).all()
    file_name = "bank_accounts.csv"
    
    # Write data to CSV file
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["account_id", "name_of_bank", "balance"])
        for account in bank_accounts:
            writer.writerow([
                account.account_id,
                #account.account_no,
                account.name_of_bank,
                account.balance,
                #account.user_id,
            ])
    
    # Upload to S3
    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/bank_account/{account_id}", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def read_bank_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return db_account


@app.put("/bank_account/{account_id}", tags=["BANK ACCOUNT"], response_model=schemas.BankAccount)
def update_bank_account(account_id: int, bank_account: schemas.BankAccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db_account.balance = bank_account.balance
    db_account.name_of_bank = bank_account.name_of_bank
    db.commit()
    db.refresh(db_account)
    return db_account


@app.delete("/bank_account/{account_id}", tags=["BANK ACCOUNT"])
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.BankAccount).filter(models.BankAccount.account_id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db.delete(db_account)
    db.commit()
    return {"Message": "Records deleted"}

# CATEGORY
@app.post("/categories/", tags=["CATEGORY"], response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    if category.category_type == "Income":
        category_id = 1
    elif category.category_type == "Expense":
        category_id = 2
    db_category = models.Category( category_type=category.category_type, category_id=category_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/upload",tags=["CATEGORY"])
def upload_category_to_s3(db:Session=Depends(get_db)):
    categories=db.query(models.Category).all()
    file_name="categories.csv"

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["category_id", "category_type"])
        for category in categories:
            writer.writerow([
                category.category_id,
                category.category_type])
                
    try:
        file_url = upload_to_s3(file_name, BUCKET_NAME)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''@app.get("/categories/", tags=["CATEGORY"], response_model=List[schemas.Category])
def read_category(db: Session = Depends(get_db)):
    db_category = db.query(models.Category).all()
    return db_category'''


@app.get("/categories/{category_id}", tags=["CATEGORY"], response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    if category_id not in [1, 2]:  # Validating that only 1 or 2 can exist
        raise HTTPException(status_code=404, detail="Category not found")
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.put("/categories/{category_id}", tags=["CATEGORY"], response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.category_type = category.category_type
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}", tags=["CATEGORY"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"Message": "Records deleted"}

import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_name, bucket_name,object_name=None):
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
