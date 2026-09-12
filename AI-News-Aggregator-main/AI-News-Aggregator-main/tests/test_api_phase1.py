import pytest
import httpx
from app.server import app
from app.database.connection import init_db

@pytest.mark.anyio
async def test_health_endpoint():
    init_db()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert "vector_store" in data

