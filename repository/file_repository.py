import pandas as pd
from sqlalchemy.orm import Session
from repository.income_repository import IncomeRepository
from repository.expense_repository import ExpenseRepository

def generate_csv_from_data(uow, db: Session) -> pd.DataFrame:
    """
    Generates a CSV DataFrame for income and expense data.

    Args:
        uow (UnitOfWork): The unit of work that provides access to the session.
        db (Session): The database session.

    Returns:
        pd.DataFrame: The CSV-formatted data for income and expenses.
    """
    # Fetch income and expense data within the scope of a Unit of Work
    with uow:
        # Use repositories to fetch data
        income_data = IncomeRepository(uow.session).get_all_incomes(db)
        expense_data = ExpenseRepository(uow.session).get_all_expenses(db)

    # Convert SQLAlchemy query results into pandas DataFrames
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

    # Concatenate both DataFrames into one
    all_data_df = pd.concat([income_df, expense_df], ignore_index=True)

    return all_data_df
