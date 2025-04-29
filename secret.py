from google.cloud import secretmanager
from google.oauth2 import service_account
import json
from google.oauth2 import service_account


def get_secret_value(secret_name: str, project_id: str, secret_version: str = "latest", key_path: str = '/path/to/your/service-account-file.json'):
    """
    Fetches the secret value from Google Cloud Secret Manager.

    :param secret_name: The name of the secret in Secret Manager
    :param project_id: Your Google Cloud project ID
    :param secret_version: The version of the secret to fetch (default is "latest")
    :param key_path: The path to your service account JSON credentials file
    :return: The value of the secret as a string
    """
    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # Create the Secret Manager client
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)

    # Construct the secret path
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"

    # Access the secret version
    response = client.access_secret_version(request={"name": secret_path})

    # Decode and return the secret value
    secret_value = response.payload.data.decode("UTF-8")
    return secret_value

def get_credentials():
    """
    Fetches the MongoDB and Gemini API keys from Google Cloud Secret Manager.
    
    :return: A dictionary containing MongoDB and Gemini API keys
    """
    # Your Google Cloud project ID
    project_id = 'the-mesh-458219-a9'

    # Path to your service account JSON file
    key_path = '/tmp/credentials.json'

    # Fetch MongoDB key
    mongo_secret_name = 'MONGODB_URI'
    mongo_secret_value = get_secret_value(mongo_secret_name, project_id, key_path=key_path)

    # Fetch Gemini API key
    gemini_secret_name = 'GEMINI_API_KEY'
    gemini_secret_value = get_secret_value(gemini_secret_name, project_id, key_path=key_path)

    # Return the keys as a dictionary
    return {
        "mongo_db_key": mongo_secret_value,
        "gemini_api_key": gemini_secret_value
    }
