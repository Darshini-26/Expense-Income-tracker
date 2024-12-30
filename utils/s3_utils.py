import boto3
from botocore.exceptions import NoCredentialsError
import os
from typing import Optional

# Initialize boto3 client
s3_client = boto3.client('s3')

# Upload data to S3
def upload_to_s3(file_path: str, bucket_name: str, s3_file_name: Optional[str] = None):
    try:
        if not s3_file_name:
            s3_file_name = os.path.basename(file_path)
        
        s3_client.upload_file(file_path, bucket_name, s3_file_name)
        print(f"Upload Successful: {file_path} to {bucket_name}/{s3_file_name}")
        return f"s3://{bucket_name}/{s3_file_name}"
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except NoCredentialsError:
        print("Credentials not available.")
        raise

# Download data from S3
def download_from_s3(bucket_name: str, s3_file_name: str, local_file_path: str):
    try:
        s3_client.download_file(bucket_name, s3_file_name, local_file_path)
        print(f"Download Successful: {bucket_name}/{s3_file_name} to {local_file_path}")
    except NoCredentialsError:
        print("Credentials not available.")
        raise
