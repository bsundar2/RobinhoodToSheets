import os
import boto3
import base64

from src.constants.common import UTF_8


def is_base64(s: str):
    """Check if a string is base64 encoded."""
    try:
        # Try to decode the string and check if it is valid base64
        return base64.b64encode(base64.b64decode(s)).decode(UTF_8) == s
    except Exception:
        return False


def decrypt_kms_value(encrypted_value):
    """Decrypt a base64-encoded KMS-encrypted value using AWS KMS."""
    kms_client = boto3.client('kms')
    decrypted_value = kms_client.decrypt(
        CiphertextBlob=base64.b64decode(encrypted_value)
    )['Plaintext'].decode(UTF_8)
    return decrypted_value


def lambda_handler(event, context):
    # Retrieve the environment variable
    secret_value = os.getenv('SECRET_ENV_VAR')

    if secret_value and is_base64(secret_value):
        # If the value appears to be base64-encoded (likely encrypted), decrypt it
        print("Encrypted value detected, attempting to decrypt...")
        try:
            decrypted_value = decrypt_kms_value(secret_value)
            print(f"Decrypted value: {decrypted_value}")
        except Exception as e:
            print(f"Error during decryption: {e}")
    else:
        # If it's not encrypted, just use the plain text value
        print(f"Plaintext value: {secret_value}")