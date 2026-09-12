import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database.connection import init_db
from app.database.chroma import chroma_store
from app.api.scheduler import scheduler, init_scheduler_jobs

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize relational database tables (PostgreSQL/SQLite) & ChromaDB
    init_db()
    print("[SERVER] Relational database & ChromaDB vector store initialized successfully.")
    
    # Start APScheduler & load user jobs
    scheduler.start()
    await init_scheduler_jobs()
    print("[SERVER] APScheduler background engine started.")
    
    yield
    
    # Shutdown: Stop scheduler
    if scheduler.running:
        scheduler.shutdown()
        print("[SERVER] APScheduler shut down cleanly.")

app = FastAPI(
    title="AI News Intelligence & Agentic RAG Platform",
    description="100% Python Backend powered by FastAPI, LangChain, LangGraph, ChromaDB, PostgreSQL & Groq LLM",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.routes.users import router as users_router
from app.api.routes.news import router as news_router
from app.api.routes.schedule import router as schedule_router
from app.api.routes.internal import router as internal_router

app.include_router(users_router)
app.include_router(news_router)
app.include_router(schedule_router)
app.include_router(internal_router)

@app.get("/api/health")
async def health_check():
    """Health check route verifying FastAPI, ChromaDB, and APScheduler status."""
    chroma_count = chroma_store.collection.count() if hasattr(chroma_store, "collection") else 0
    return {
        "status": "healthy",
        "database": "PostgreSQL / SQLite",
        "vector_store": "ChromaDB (Local Persistent)",
        "vector_count": chroma_count,
        "scheduler": "running" if scheduler.running else "stopped",
        "service": "100% Python AI News Intelligence & Agentic RAG Platform"
    }

# Serve React static production build if compiled
dist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static_frontend")
