from google.cloud import secretmanager
import google.auth
import json
import os
from dotenv import load_dotenv

def get_secret(name: str, version: str = "latest") -> str:
    """
    Universal secret loader:
    1. LOCAL (no GCP credentials): read from environment variable.
    2. CLOUD RUN / GCP: read from Secret Manager if project ID exists.
    """

    # 1️⃣ LOCAL：優先使用環境變數
    env_value = os.environ.get(name)
    if env_value:
        return env_value

    # 2️⃣ CLOUD：需要 GCP project + Secret Manager
    project_id = (
        os.environ.get("GCP_PROJECT")
        or os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("GCLOUD_PROJECT")
    )

    # 若沒有 project_id → 無法讀 Secret Manager
    if not project_id:
        raise RuntimeError(
            f"Environment variable '{name}' not found, and no GCP project ID available. "
            "Set the environment variable when running locally."
        )

    # 若沒有 secretmanager 客戶端 → 無法讀 Secret Manager
    if secretmanager is None:
        raise RuntimeError(
            f"Secret Manager client unavailable, and environment variable '{name}' not set."
        )

    # 3️⃣ 讀 Secret Manager
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project_id}/secrets/{name}/versions/{version}"
    response = client.access_secret_version(name=secret_path)
    return response.payload.data.decode("UTF-8")
