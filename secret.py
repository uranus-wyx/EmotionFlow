from google.cloud import secretmanager
import google.auth
import json
import os
from dotenv import load_dotenv

def get_secret(secret_id: str, version: str = "latest") -> str:
    # project_id = os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_CLOUD_PROJECT")
    project_id = "the-mesh-458219-a9"
    if not project_id:
        raise RuntimeError("GCP project ID not found in environment variables.")

    # 建立 Secret Manager 客戶端
    client = secretmanager.SecretManagerServiceClient()

    # 建立 Secret 路徑：projects/{project_id}/secrets/{secret_id}/versions/{version}
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"

    # 存取 Secret 版本
    response = client.access_secret_version(name=secret_name)

    # 回傳 Secret 的值（以 UTF-8 解碼）
    return response.payload.data.decode("UTF-8")
