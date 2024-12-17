
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

def get_ssm_parameter(name, with_decryption=True,region_name=None):
    """
    Retrieves a parameter from AWS SSM Parameter Store.

    Args:
        name (str): The name of the parameter.
        with_decryption (bool): Whether to decrypt the parameter value (for SecureString).

    Returns:
        str: The parameter value.
    """
    print(f"Retrieving parameter: {name}")
    try:
        region_name = region_name or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        ssm_client = boto3.client('ssm', region_name=region_name) 
        response = ssm_client.get_parameter(
            Name=name,
            WithDecryption=with_decryption
        )
        return response['Parameter']['Value']
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found.")
    except PartialCredentialsError:
        raise RuntimeError("Incomplete AWS credentials.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving SSM parameter: {e}")
