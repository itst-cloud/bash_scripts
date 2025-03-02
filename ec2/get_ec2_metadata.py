import requests

# EC2 metadata service URLs
METADATA_URL = "http://169.254.169.254/latest/meta-data/"
TOKEN_URL = "http://169.254.169.254/latest/api/token"

# Try to get an IMDSv2 token
try:
    token_response = requests.put(TOKEN_URL, headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"})
    if token_response.status_code == 200:
        token = token_response.text
        headers = {"X-aws-ec2-metadata-token": token}  # IMDSv2
    else:
        headers = {}  # Fallback to IMDSv1
except requests.exceptions.RequestException:
    headers = {}  # Assume IMDSv1

# Function to get EC2 metadata with error handling
def get_metadata(path):
    try:
        response = requests.get(METADATA_URL + path, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text.strip() if response.text else None
    except requests.exceptions.RequestException:
        return None

# Retrieve instance details
instance_id = get_metadata("instance-id")
hostname = get_metadata("hostname")
iam_role = get_metadata("iam/security-credentials/")

print(f"Instance ID: {instance_id}")
print(f"Hostname: {hostname}")

# Retrieve IAM credentials only if an IAM role exists
if iam_role:
    print(f"IAM Role: {iam_role}")
    iam_credentials_json = get_metadata(f"iam/security-credentials/{iam_role}")

    if iam_credentials_json:
        try:
            iam_credentials = requests.get(METADATA_URL + f"iam/security-credentials/{iam_role}", headers=headers).json()
            print("Temporary AWS Credentials:")
            print(f"Access Key: {iam_credentials.get('AccessKeyId', 'N/A')}")
            print(f"Secret Key: {iam_credentials.get('SecretAccessKey', 'N/A')}")
            print(f"Token: {iam_credentials.get('Token', 'N/A')}")
            print(f"Expiration: {iam_credentials.get('Expiration', 'N/A')}")
        except requests.exceptions.JSONDecodeError:
            print("Error decoding IAM credentials JSON response.")
    else:
        print("No IAM credentials found.")
else:
    print("No IAM role assigned to this instance.")
