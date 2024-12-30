import pandas as pd
from sqlalchemy.orm import Session
from models.models import Income, Expense

def generate_csv_from_data(db: Session) -> pd.DataFrame:
    """
    Generates a CSV DataFrame for income and expense data.

    Args:
        db (Session): The database session.

    Returns:
        pd.DataFrame: The CSV-formatted data for income and expenses.
    """
    # Query the database for income and expense data
    incomes = db.query(Income).all()
    expenses = db.query(Expense).all()

    # Directly convert SQLAlchemy query result into a pandas DataFrame
    income_df = pd.read_sql(db.query(Income).statement, db.bind)
    expense_df = pd.read_sql(db.query(Expense).statement, db.bind)

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

    return all_data_df
