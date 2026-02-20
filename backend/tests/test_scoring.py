from app.scoring.engine import ScoringEngine
from app.schemas import ClaimScoreRequest

def test_low_risk_claim():
    claim = ClaimScoreRequest(
        claim_id="TEST-001",
        customer_id="CUST-001",
        amount=400,
        incident_type="collision",
        history_score=20
    )
    
    risk_score, fraud_prob, decision = ScoringEngine.calculate_risk_score(claim)
    
    assert risk_score < 50
    assert fraud_prob < 0.35
    assert decision == "APPROVE"

def test_high_risk_claim():
    claim = ClaimScoreRequest(
        claim_id="TEST-002",
        customer_id="CUST-002",
        amount=50000,
        incident_type="fire",
        history_score=80
    )
    
    risk_score, fraud_prob, decision = ScoringEngine.calculate_risk_score(claim)
    
    assert risk_score > 70
    assert fraud_prob > 0.70
    assert decision == "REJECT"

def test_risk_score_cap():
    claim = ClaimScoreRequest(
        claim_id="TEST-003",
        customer_id="CUST-003",
        amount=100000,
        incident_type="fire",
        history_score=100
    )
    
    risk_score, _, _ = ScoringEngine.calculate_risk_score(claim)
    
    assert risk_score <= 100
