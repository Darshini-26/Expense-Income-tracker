import os
import pandas as pd
from sqlalchemy.orm import Session
from repository.s3_repository import upload_to_s3
from models.models import Income, Expense, BankAccount, Category

BUCKET_NAME = "financial-tracker1"

def upload_data_to_s3(db: Session, model, file_name: str, columns: list = None) -> str:
    """
    Fetch data from the database, save it as a CSV file, and upload it to S3.

    Args:
        db (Session): Database session.
        model (SQLAlchemy Model): The model to query data from.
        file_name (str): The name of the CSV file to generate.
        columns (list, optional): The columns to include in the CSV. Defaults to None.

    Returns:
        str: The URL of the uploaded file.
    """
    # Fetch data and convert to DataFrame
    data_df = pd.read_sql(db.query(model).statement, db.bind)

    # If specific columns are provided, filter the DataFrame
    if columns:
        data_df = data_df[columns]

    # Write to a CSV file
    data_df.to_csv(file_name, index=False)

    try:
        # Upload the file to S3
        file_url = upload_to_s3(file_name, BUCKET_NAME)

        # Remove the local file
        os.remove(file_name)

        return file_url
    except Exception as e:
        # Remove the file if an exception occurs
        if os.path.exists(file_name):
            os.remove(file_name)
        raise e
