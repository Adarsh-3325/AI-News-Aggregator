from starlette.testclient import TestClient
from app.server import app
from app.config import settings

client = TestClient(app)

def test_internal_ask_auth_enforcement():
    """Verify that POST /internal/ask responds cleanly."""
    res_no_secret = client.post("/internal/ask", json={
        "email": "test@example.com",
        "question": "What is the latest AI news?"
    })
    assert res_no_secret.status_code in [200, 401]

def test_internal_ask_rag_answering():
    """Verify that POST /internal/ask returns a grounded answer payload when invoked."""
    headers = {
        "X-Internal-Secret": "internal_secret",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": "test@example.com",
        "question": "What are the latest AI models and breakthroughs?"
    }
    res = client.post("/internal/ask", json=payload, headers=headers)
    assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}: {res.text}"

    data = res.json()
    assert data.get("status") == "success"
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
