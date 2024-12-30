import io
import pandas as pd
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from repository.s3_repository import upload_to_s3  # Assuming you have this function implemented
from repository.file_repository import generate_csv_from_data  # Assuming this function generates the DataFrame from database

def upload_file_to_s3(file: io.BytesIO, bucket_name: str, s3_file_name: str) -> str:
    """
    Uploads a file (not generated from database, but uploaded by the user) to S3.

    Args:
        file (io.BytesIO): The file to upload (in-memory).
        bucket_name (str): The S3 bucket name.
        s3_file_name (str): The file name to store in S3.

    Returns:
        str: The S3 URL of the uploaded file.
    """
    return upload_to_s3(file, bucket_name, s3_file_name)

def download_data_as_csv(db: Session) -> StreamingResponse:
    """
    Downloads income and expense data as a CSV file.

    Args:
        db (Session): The database session.

    Returns:
        StreamingResponse: A CSV file of income and expense data.
    """
    # Generate CSV file from income and expense data
    all_data_df = generate_csv_from_data(db)

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
