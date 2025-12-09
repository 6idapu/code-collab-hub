# Yandex Cloud Deploy Guide

This guide explains how to deploy this application to Yandex Cloud using Container Registry and Serverless Containers. It assumes you already have `yc` CLI installed and configured, and you have a working Yandex Cloud account.

## Quick Prerequisites
- Install `yc` CLI: `curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash`
- Authenticate locally: `yc init` or use a service account key to auth during automation.
- Create a Yandex Container Registry and repository.
- Create a Managed PostgreSQL instance and note the connection URI.
- The project folder id for this repository is: `b1geur9773l61i3b3a7a`.

## Recommended GitHub Secrets
- `YC_SA_KEY` — Yandex service account key JSON contents (create a service account with permissions to push images and manage serverless containers).
- `YC_FOLDER_ID` — Yandex Cloud folder ID (we used `b1geur9773l61i3b3a7a`).
- `YC_REGISTRY_NAME` — The registry name you created in Yandex Cloud.
- `YC_REGISTRY_URL` — Registry URL (e.g. `cr.yandex/<REGISTRY_ID>`).
 - `YC_SERVICE_NAME` — Name for the serverless container service (e.g., `code-collab-hub`).
 - `YC_REGION` — Yandex region (e.g. `ru-central1`).

## Steps (Manual)

1. Build & push image locally (alternatively use the GitHub Action):

```bash
# Build
docker build -t ${YC_REGISTRY_URL}/code-collab-hub:latest .

# Log in (after activating service account):
yc auth activate-service-account --key-file /path/to/yc-key.json
eval "$(yc container registry get-login --registry-name $YC_REGISTRY_NAME --folder-id $YC_FOLDER_ID)"

# Push
docker push ${YC_REGISTRY_URL}/code-collab-hub:latest
```

2. Create (or update) Serverless Container service in the Console
- Console → Serverless → Serverless Containers → Create service (select Docker image)
- Choose region, memory, concurrency and set env vars:
  - `DATABASE_URL` → your managed Postgres URI (not SQLite)
  - `ENV=production`

3. Health check: set `/api/v1/health`.

4. Confirm logs and access the URL provided by Yandex.

## Steps (CI/CD with GitHub Actions)
- Add the GitHub secrets above: `YC_SA_KEY`, `YC_FOLDER_ID`, `YC_REGISTRY_NAME`, `YC_REGISTRY_URL`.
- The included workflow `.github/workflows/push-to-yandex.yml` builds and pushes images on `main` push.

## Example `yc` commands to create registry and serverless container

```bash
# Create registry
yc container registry create --name my-registry --folder-id $YC_FOLDER_ID

# Create repository inside registry
yc container repository create --registry-name my-registry --name code-collab-hub --folder-id $YC_FOLDER_ID

# Create a serverless container service (replace <REGION>)
yc serverless container create --name code-collab-hub --folder-id $YC_FOLDER_ID --memory 512M --concurrency 50 --region ru-central1

# Add new version referencing the pushed image
yc serverless container version create --service-name code-collab-hub --container-image ${YC_REGISTRY_URL}/code-collab-hub:latest

# Activate version (if needed) - usually release created implicitly on version create
```

## Notes
- You must set a managed Postgres `DATABASE_URL` in the service environment.
- Ensure your service account has permissions to push to registry and to create/update serverless services.
- If your DB is not publicly available, use VPC connector or set the serverless container's network settings to the same VPC.
