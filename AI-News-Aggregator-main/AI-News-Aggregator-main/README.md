<div align="center">

# ⚡ AI News Intelligence & Agentic RAG Platform
### Autonomous News Ingestion | Agentic RAG | Personalized Delivery (100% Python Architecture)

[![FastAPI](https://img.shields.io/badge/FastAPI-100%25_Python-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_RAG-blue?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-7C3AED?style=for-the-badge)](https://www.trychroma.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relational_DB-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![FastEmbed](https://img.shields.io/badge/FastEmbed-BAAI%2Fbge--small--en--v1.5-D97706?style=for-the-badge)](https://github.com/qdrant/fastembed)
[![Groq LLM](https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=for-the-badge)](https://groq.com)
[![React 19](https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev)

<br/>

**[System Architecture Flow Diagram](#-software-architecture-flow-diagram)** • **[Core Workflow](#-agentic-rag-workflow)** • **[Features](#-key-features)** • **[Quickstart](#-local-development-setup)**

</div>

---

## 📖 Overview

The **AI News Intelligence & Agentic RAG Platform** is a production-ready, 100% Python backend platform designed for autonomous multi-channel news ingestion, LLM anti-hype distillation, vector similarity search, and citation-backed question answering.

> [!NOTE]
> **No Express.js | No MongoDB | 100% Python Backend | Production Ready**
>
> All backend operations run natively on **FastAPI**, **LangChain**, **LangGraph**, **ChromaDB**, and **PostgreSQL** (with SQLite fallback).

---

## 🎨 Software Architecture Flow Diagram

![AI News Intelligence & Agentic RAG Platform Architecture Diagram](architecture_diagram.svg)

---

## 🚀 Core Architectural Highlights

1. **1. Data Sources (Ingestion):**
   - **Google News RSS**: Real-time articles across custom categories.
   - **YouTube**: Automated video transcript scraping.
   - **Open-Meteo**: Weather forecast updates.
   - **Other Sources**: Tech, Markets, Startups, Geopolitics.

2. **2. Ingestion Pipeline (ETL + Processing):**
   - **Fetch & Parse**: Scrapers and RSS parsing.
   - **Clean & Normalize**: Noise removal and URL deduplication.
   - **Extract Metadata**: Titles, dates, categories, sources.
   - **Generate Summary**: Anti-hype 3-bullet distillation via **Groq LLM**.

3. **3. Local Embedding Generation (FastEmbed):**
   - Local CPU execution using `BAAI/bge-small-en-v1.5` ONNX model.
   - Generates **384-dimensional dense vectors** with zero API cost.

4. **4. Dual Storage Layer:**
   - **PostgreSQL**: Relational schema for Users, Preferences, Articles, Digests, Sent Logs, and Agent Run History via SQLAlchemy.
   - **ChromaDB**: Local, persistent vector store for article embeddings and cosine similarity search.

5. **5. LangGraph Agent (Agentic RAG Centerpiece):**
   - **6-Stage StateGraph Workflow**:
     1. *Query Analysis & Routing*: Analyzes user query and selects tool pipeline.
     2. *Retrieval*: Performs ChromaDB vector similarity search.
     3. *Relevance Check*: Evaluates similarity threshold (>= 0.50).
     4. *Live Research (Conditional Fallback)*: Calls Brave / Google Search APIs if vector score is weak.
     5. *Evidence Verification*: Validates, deduplicates, and filters sources.
     6. *Synthesis*: Generates grounded answer with explicit inline citations via **Groq LLM**.
   - **Connected Tools**: Vector Search Tool, Live Web Search Tool, News Retrieval Tool, YouTube Transcript Tool, Weather Tool, Utility Tools.

6. **6. Scheduled News Digest (APScheduler):**
   - Automated background jobs in Python via `APScheduler`.
   - Personalized topic weighting and Gmail SMTP delivery.

7. **7. FastAPI Backend & React Frontend:**
   - **FastAPI**: 100% Python REST API handling users, digests, search, and agent execution.
   - **React + Vite**: Interactive frontend with News Feed, Ask AI Chat, and Topic Preference controls.

---

## 💻 Local Development Setup

### 1. Prerequisites
- **Python** $\ge$ 3.10
- **Node.js** $\ge$ 18.x
- **Groq API Key** (Free at [console.groq.com](https://console.groq.com))

---

### 2. Environment Variables Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure settings:
```env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./news_aggregator.db
CHROMA_PERSIST_DIR=./chroma_db
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

### 3. Run FastAPI Backend (Port 8000)
```bash
pip install -r requirements.txt
uvicorn app.server:app --host 127.0.0.1 --port 8000 --reload
```

---

### 4. Run React Frontend (Port 5173)
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to interact with the platform.

---

## 🌐 Cloud Deployment Guide (Render & Docker)

### Option 1: Native Python Web Service on Render (Recommended)

1. Create a new **Web Service** on [Render](https://dashboard.render.com/).
2. Connect repository: `https://github.com/Adarsh-3325/AI-News-Aggregator`.
3. Set the following parameters:
   - **Runtime**: `Python 3`
   - **Environment Variable**: `PYTHON_VERSION` = `3.12.0`
   - **Build Command**:
     ```bash
     python -c "import os; [os.chdir(r) for r, d, f in os.walk('.') if 'requirements.txt' in f and 'node_modules' not in r]; print('Found requirements.txt in:', os.getcwd()); os.system('pip install -r requirements.txt')" && (cd frontend 2>/dev/null || cd AI-News-Aggregator-main/frontend 2>/dev/null || cd */frontend 2>/dev/null) && npm install && npm run build
     ```
   - **Start Command**:
     ```bash
     python -c "import os; [os.chdir(r) for r, d, f in os.walk('.') if 'start.sh' in f and 'node_modules' not in r]; os.system('./start.sh')" || uvicorn app.server:app --host 0.0.0.0 --port $PORT
     ```

### Option 2: Render Blueprint / Docker Container

Deploy using the multi-stage [`Dockerfile`](file:///c:/Users/adars/Downloads/AI-News-Aggregator-main/AI-News-Aggregator-main/Dockerfile) or automated [`render.yaml`](file:///c:/Users/adars/Downloads/AI-News-Aggregator-main/AI-News-Aggregator-main/render.yaml) Blueprint:
- **Stage 1 (Node.js 20)**: Compiles React SPA (`npm run build`).
- **Stage 2 (Python 3.12)**: Serves static UI + FastAPI REST endpoints on port `8000`.

---

## ⏰ Automated GitHub Actions Scheduler

The platform includes a built-in automated workflow ([`.github/workflows/daily_digest.yml`](file:///c:/Users/adars/Downloads/AI-News-Aggregator-main/AI-News-Aggregator-main/.github/workflows/daily_digest.yml)) that runs daily at **11:00 PM IST (17:30 UTC)** or manually via **workflow_dispatch**.

### Setup GitHub Secrets:
Navigate to `Settings` -> `Secrets and variables` -> `Actions` in your GitHub repository and add:

| Secret Name | Description |
| :--- | :--- |
| `GROQ_API_KEY` | Groq API Key for LLM summarization |
| `EMAIL_USER` | Sender Gmail address |
| `EMAIL_APP_PASSWORD` | 16-character Google App Password |
| `RECIPIENT_EMAIL` | Target email address for daily digest |
| `BRAVE_API_KEY` | (Optional) Brave Search API Key |

### Manual Execution:
Go to **Actions Tab** → Click **Automated AI News Intelligence & Email Digest** → Click **Run workflow**.

---

## 📄 License

Distributed under the **MIT License**.

