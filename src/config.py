
from src.aws_ssm import get_ssm_parameter  # Import the function from aws_ssm.py

def get_database_url():
    """
    Retrieves the database URL from AWS SSM Parameter Store.
    
    Returns:
        str: The database URL retrieved from the SSM parameter store.
    """
    try:
        database_url = get_ssm_parameter('database-url')  # Call the imported function
        if database_url is None:
            raise RuntimeError("Failed to retrieve the database URL.")
        return database_url
    except Exception as e:
        raise RuntimeError(f"Error retrieving database URL: {e}")




