#!/bin/sh
set -e

echo "🚀 Starting 100% Python AI News Intelligence & Agentic RAG Platform..."
exec uvicorn app.server:app --host 0.0.0.0 --port ${PORT:-8000}

