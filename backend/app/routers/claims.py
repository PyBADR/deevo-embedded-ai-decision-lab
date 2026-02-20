from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import ClaimScoreRequest, ClaimScoreResponse
from app.models import Decision, AuditLog
from app.scoring.engine import ScoringEngine
from app.clients.mongo import mongo_client
from app.clients.ollama import ollama_client
from app.dependencies import verify_api_key
from app.utils.logging import get_logger, get_trace_id, set_trace_id
from app.config import settings
import uuid

router = APIRouter()
logger = get_logger(__name__)

@router.post("/api/claim/score", response_model=ClaimScoreResponse)
async def score_claim(
    claim: ClaimScoreRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Score a claim and return decision."""
    # Set trace ID for this request
    set_trace_id(str(uuid.uuid4()))
    trace_id = get_trace_id()
    
    logger.info(f"Scoring claim {claim.claim_id} (trace: {trace_id})")
    
    try:
        # Calculate risk score
        risk_score, fraud_probability, decision = ScoringEngine.calculate_risk_score(claim)
        
        # Generate explanation (try Ollama first, fallback to template)
        explanation = await ollama_client.generate_explanation(
            claim.amount, claim.incident_type, claim.history_score,
            risk_score, fraud_probability
        )
        
        if not explanation:
            explanation = ScoringEngine.generate_template_explanation(
                claim, risk_score, fraud_probability, decision
            )
        
        # Create decision record
        decision_record = Decision(
            claim_id=claim.claim_id,
            customer_id=claim.customer_id,
            model_version=settings.MODEL_VERSION,
            policy_version=settings.POLICY_VERSION,
            risk_score=risk_score,
            fraud_probability=fraud_probability,
            decision=decision,
            explanation=explanation
        )
        
        db.add(decision_record)
        db.flush()
        
        # Create audit log
        audit_event = AuditLog(
            decision_id=decision_record.decision_id,
            event_type="decision_created",
            event_payload={
                "trace_id": trace_id,
                "input": claim.model_dump(),
                "output": {
                    "risk_score": risk_score,
                    "fraud_probability": fraud_probability,
                    "decision": decision
                }
            }
        )
        
        db.add(audit_event)
        db.commit()
        db.refresh(decision_record)
        
        # Store in MongoDB
        mongo_client.store_claim(
            claim.claim_id,
            claim.customer_id,
            claim.model_dump(),
            str(decision_record.decision_id)
        )
        
        logger.info(f"Decision {decision_record.decision_id}: {decision} (trace: {trace_id})")
        
        return ClaimScoreResponse(
            decision_id=decision_record.decision_id,
            claim_id=decision_record.claim_id,
            customer_id=decision_record.customer_id,
            risk_score=decision_record.risk_score,
            fraud_probability=decision_record.fraud_probability,
            decision=decision_record.decision,
            explanation=decision_record.explanation,
            model_version=decision_record.model_version,
            policy_version=decision_record.policy_version,
            timestamp=decision_record.created_at
        )
    
    except Exception as e:
        logger.error(f"Error scoring claim: {e} (trace: {trace_id})")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")
