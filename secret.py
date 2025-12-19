import os

try:
    from google.cloud import secretmanager
except ImportError:
    secretmanager = None


def get_secret(name: str, version: str = "latest") -> str:
    """
    通用版 secret loader：
    1. 先看環境變數（本機 & Cloud Run 都適用）
    2. 若沒找到且有 GCP project id，就嘗試用 Secret Manager
    """

    # 1️⃣ 先用環境變數（local / Cloud Run 都很好用）
    env_value = os.environ.get(name)
    if env_value:
        return env_value

    # 2️⃣ 嘗試走 Secret Manager（可選）
    project_id = (
        os.environ.get("GCP_PROJECT")
        or os.environ.get("GOOGLE_CLOUD_PROJECT")
        or os.environ.get("GCLOUD_PROJECT")
    )

    if not project_id or secretmanager is None:
        # 既沒有環境變數，也沒辦法用 Secret Manager
        raise RuntimeError(
            f"Environment variable '{name}' not found, and Secret Manager is not available or project id is missing."
        )

    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project_id}/secrets/{name}/versions/{version}"
    response = client.access_secret_version(name=secret_path)
    return response.payload.data.decode("UTF-8")
