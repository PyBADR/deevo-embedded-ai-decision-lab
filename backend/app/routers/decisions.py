from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Decision, AuditLog
from app.schemas import DecisionDetail, ClaimScoreResponse
from app.scoring.engine import ScoringEngine
from typing import List

router = APIRouter()

@router.get("/api/decisions", response_model=List[ClaimScoreResponse])
async def list_decisions(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """List recent decisions."""
    decisions = db.query(Decision).order_by(
        Decision.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    return [
        ClaimScoreResponse(
            decision_id=d.decision_id,
            claim_id=d.claim_id,
            customer_id=d.customer_id,
            risk_score=d.risk_score,
            fraud_probability=d.fraud_probability,
            decision=d.decision,
            explanation=d.explanation,
            model_version=d.model_version,
            policy_version=d.policy_version,
            timestamp=d.created_at
        )
        for d in decisions
    ]

@router.get("/api/decisions/{decision_id}", response_model=DecisionDetail)
async def get_decision(decision_id: str, db: Session = Depends(get_db)):
    """Get decision detail with audit trail."""
    decision = db.query(Decision).filter(
        Decision.decision_id == decision_id
    ).first()
    
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    audit_logs = db.query(AuditLog).filter(
        AuditLog.decision_id == decision_id
    ).order_by(AuditLog.created_at).all()
    
    return DecisionDetail(
        decision=ClaimScoreResponse(
            decision_id=decision.decision_id,
            claim_id=decision.claim_id,
            customer_id=decision.customer_id,
            risk_score=decision.risk_score,
            fraud_probability=decision.fraud_probability,
            decision=decision.decision,
            explanation=decision.explanation,
            model_version=decision.model_version,
            policy_version=decision.policy_version,
            timestamp=decision.created_at
        ),
        audit_events=[
            {
                "event_type": log.event_type,
                "event_payload": log.event_payload,
                "created_at": log.created_at.isoformat()
            }
            for log in audit_logs
        ]
    )

@router.get("/api/models")
async def list_models():
    """List available models."""
    return {
        "models": [
            {
                "name": "rule-based-v1",
                "version": "rb-v1",
                "type": "deterministic",
                "status": "active"
            }
        ]
    }

@router.post("/api/seed")
async def seed_demo_data(
    count: int = Query(default=10, le=100),
    seed_token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Seed demo data (protected endpoint)."""
    from app.config import settings
    import random
    
    if seed_token != settings.SEED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid seed token")
    
    incident_types = ["collision", "theft", "fire", "injury", "vandalism"]
    
    for i in range(count):
        claim = {
            "claim_id": f"CLM-DEMO-{i+1:04d}",
            "customer_id": f"CUST-{random.randint(1000, 9999)}",
            "amount": random.uniform(500, 50000),
            "incident_type": random.choice(incident_types),
            "history_score": random.uniform(0, 100)
        }
        
        from app.schemas import ClaimScoreRequest
        claim_request = ClaimScoreRequest(**claim)
        
        risk_score, fraud_prob, decision_text = ScoringEngine.calculate_risk_score(claim_request)
        explanation = ScoringEngine.generate_template_explanation(
            claim_request, risk_score, fraud_prob, decision_text
        )
        
        decision_record = Decision(
            claim_id=claim["claim_id"],
            customer_id=claim["customer_id"],
            risk_score=risk_score,
            fraud_probability=fraud_prob,
            decision=decision_text,
            explanation=explanation
        )
        
        db.add(decision_record)
    
    db.commit()
    
    return {"message": f"Seeded {count} demo claims"}
