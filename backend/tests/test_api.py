from fastapi.testclient import TestClient
from app.main import app
from app.schemas import ClaimScoreRequest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_score_claim(override_get_db):
    claim_data = {
        "claim_id": "API-TEST-001",
        "customer_id": "CUST-999",
        "amount": 3000,
        "incident_type": "collision",
        "history_score": 45
    }
    
    response = client.post("/api/claim/score", json=claim_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "decision_id" in data
    assert data["decision"] in ["APPROVE", "REVIEW", "REJECT"]
    assert "risk_score" in data
    assert "fraud_probability" in data

def test_list_decisions(override_get_db):
    response = client.get("/api/decisions?limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
