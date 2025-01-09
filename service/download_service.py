import pandas as pd
import io
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from service.unit_of_work import UnitOfWork
from models import models

def download_incomes_expenses_as_csv(uow: UnitOfWork):
    try:
        # Fetch data using UnitOfWork
        income_query = uow._session.query(models.Income).statement
        expense_query = uow._session.query(models.Expense).statement

        # Convert SQLAlchemy query results into pandas DataFrames
        income_df = pd.read_sql(income_query, uow._session.bind)
        expense_df = pd.read_sql(expense_query, uow._session.bind)

        # Add "Type" column to differentiate between Income and Expense
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

        # Create an in-memory CSV file
        output = io.StringIO()
        all_data_df.to_csv(output, index=False)

        # Reset file pointer to the beginning
        output.seek(0)

        # Return the CSV as a streaming response
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CSV: {str(e)}")
