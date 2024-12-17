#DATABASE_URL = "postgresql://postgres:mydbinstance@financetracker-db.cpkyou0kgufa.us-east-1.rds.amazonaws.com:5432/postgres"


# from pydantic_settings import BaseSettings
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




'''class Settings(BaseSettings):
    """
    Application settings, including database configuration.
    """
    ssm_db_parameter: str = "/financetracker/database-url"  # Default SSM parameter name

    @property
    def database_url(self):
        """
        Fetch the database URL from SSM Parameter Store.
        """
        return get_ssm_parameter(self.ssm_db_parameter)

# Instantiate the settings object
settings = Settings()'''
