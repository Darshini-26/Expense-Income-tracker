import boto3
from botocore.exceptions import NoCredentialsError

BUCKET_NAME = "financial-tracker1"
def upload_to_s3(file_name: str, bucket_name: str, object_name: str = None) -> str:
    """
    Uploads a file to an S3 bucket.

    Args:
        file_name (str): The path to the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str, optional): The S3 object name. If not specified, the file name is used.

    Returns:
        str: The URL of the uploaded file.

    Raises:
        Exception: If the file is not found or credentials are unavailable.
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # If object_name is not provided, use file_name as the object name
    if object_name is None:
        object_name = file_name

    try:
        # Upload the file to the specified S3 bucket
        s3_client.upload_file(file_name, bucket_name, object_name)

        # Return the S3 URL of the uploaded file
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except FileNotFoundError:
        raise Exception("The file was not found")
    except NoCredentialsError:
        raise Exception("AWS credentials not available")
