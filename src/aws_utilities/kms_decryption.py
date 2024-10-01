
import boto3
import base64

from src.constants.aws import KMS, KMS_PLAINTEXT, US_WEST_REGION
from src.constants.common import UTF_8


def is_base64(s: str):
    """Check if a string is base64 encoded."""
    try:
        # Try to decode the string and check if it is valid base64
        return base64.b64encode(base64.b64decode(s)).decode(UTF_8) == s
    except Exception:
        print("Encountered an exception while decoding string using base64. Returning false.")
        return False


def decrypt_kms_value(encrypted_value):
    """Decrypt a base64-encoded KMS-encrypted value using AWS KMS."""
    kms_client = boto3.client(KMS, region_name=US_WEST_REGION)
    decrypted_value = kms_client.decrypt(
        CiphertextBlob=base64.b64decode(encrypted_value)
    )[KMS_PLAINTEXT].decode(UTF_8)
    return decrypted_value
