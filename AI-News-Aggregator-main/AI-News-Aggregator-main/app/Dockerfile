# ==========================================================
# STAGE 1: Build React Frontend Static Assets
# ==========================================================
FROM node:20-alpine AS frontend-builder
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ==========================================================
# STAGE 2: 100% Python FastAPI Backend + LangGraph Agent
# ==========================================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependency specifications
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY main.py .

# Copy compiled React frontend assets from Stage 1
COPY --from=frontend-builder /build/frontend/dist ./frontend/dist

# Create directory for ChromaDB vector store
RUN mkdir -p /app/chroma_db

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Start FastAPI application (serves API endpoints + static React frontend)
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]

