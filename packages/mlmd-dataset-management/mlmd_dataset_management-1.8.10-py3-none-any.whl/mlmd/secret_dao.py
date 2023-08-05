
import json
from google.cloud import secretmanager
import os

def get_secret(secret_name, secret_version=None, project_id="mlops-315607", json_decode=True):
	if secret_version is None:
		secret_version = os.environ.get("SECRET_VERSION")
	if secret_version is None:
		print("Configuration version is not defined (by using env var SECRET_VERSION) and is set to default value 1")
		secret_version = 1

	client = secretmanager.SecretManagerServiceClient()
	name = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"
	res = client.access_secret_version(request={"name":name})
	if json_decode:
		return json.loads(res.payload.data.decode("UTF-8"))
	return res.payload.data.decode("UTF-8")
