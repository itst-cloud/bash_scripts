import requests

# Base URL for EC2 instance metadata
METADATA_URL = "http://169.254.169.254/latest/meta-data/"

def get_metadata(path):
    """Helper function to get EC2 metadata with error handling."""
    try:
        response = requests.get(METADATA_URL + path, timeout=2)
        response.raise_for_status()  # Raise an error for HTTP failures (4xx, 5xx)
        return response.text.strip() if response.text else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {path}: {e}")
        return None

# Retrieve instance ID
instance_id = get_metadata("instance-id")
print(f"Instance ID: {instance_id}")

# Retrieve instance hostname
hostname = get_metadata("hostname")
print(f"Hostname: {hostname}")

# Retrieve IAM role name
iam_role = get_metadata("iam/security-credentials/")
if iam_role:
    print(f"IAM Role: {iam_role}")

    # Retrieve security credentials for the IAM role
    try:
        iam_credentials_response = requests.get(METADATA_URL + f"iam/security-credentials/{iam_role}", timeout=2)
        iam_credentials_response.raise_for_status()
        iam_credentials = iam_credentials_response.json()

        print("\nTemporary AWS Credentials:")
        print(f"Access Key: {iam_credentials.get('AccessKeyId', 'N/A')}")
        print(f"Secret Key: {iam_credentials.get('SecretAccessKey', 'N/A')}")
        print(f"Token: {iam_credentials.get('Token', 'N/A')}")
        print(f"Expiration: {iam_credentials.get('Expiration', 'N/A')}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching IAM credentials: {e}")
    except ValueError:
        print("Failed to parse IAM credentials as JSON.")
else:
    print("No IAM Role assigned to the instance.")
