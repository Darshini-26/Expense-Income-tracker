from typing import Type  # Add this import
from service.unit_of_work import UnitOfWork
from models import models
import pandas as pd
import os
from repository.s3_repository import upload_to_s3

BUCKET_NAME = "financial-tracker1"

def upload_data_to_s3(uow: UnitOfWork, model: Type[models.Base], file_name: str, columns: list = None) -> str:
    try:
        # Using the UnitOfWork context manager
        with uow:
            # Map models to repositories
            repo_mapping = {
                models.Income: uow.incomes,
                models.Expense: uow.expenses,
                models.BankAccount: uow.bank_accounts,
                models.Category: uow.categories,
            }

            # Check if the model is supported
            if model not in repo_mapping:
                raise ValueError(f"Unsupported model: {model}")

            # Access the repository
            repo = repo_mapping[model]

            # Fetch data from the repository
            data = repo.get_all()  # Assuming get_all() method exists

            # Convert the SQLAlchemy object to a list of dictionaries using __dict__
            data_dict = [
                {key: value for key, value in record.__dict__.items() if not key.startswith('_')} 
                for record in data
            ]

            # Convert to DataFrame
            data_df = pd.DataFrame(data_dict)

            # If specific columns are provided, filter the DataFrame
            if columns:
                data_df = data_df[columns]

            # Write the data to a CSV file
            data_df.to_csv(file_name, index=False)

            # Upload the file to S3
            file_url = upload_to_s3(file_name, BUCKET_NAME)

            # Optionally delete the local file after uploading
            os.remove(file_name)

            return file_url

    except Exception as e:
        # Clean up the file if an exception occurs
        if os.path.exists(file_name):
            os.remove(file_name)
        raise e
