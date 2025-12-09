## Multi-stage Dockerfile to build frontend and backend in a single container
### Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
COPY frontend/package-lock.json ./
RUN npm ci --silent
COPY frontend/ ./
RUN npm run build

### Stage 2: Build runtime
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copy and install python backend
COPY backend/ ./backend
WORKDIR /app/backend
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir ./

# Copy built frontend assets into backend static folder
WORKDIR /app
COPY --from=frontend-builder /app/frontend/dist ./backend/frontend/dist

EXPOSE 8000

WORKDIR /app/backend
CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
