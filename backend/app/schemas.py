from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class ClaimScoreRequest(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier")
    customer_id: str = Field(..., description="Customer identifier")
    amount: float = Field(..., gt=0, description="Claim amount")
    incident_type: str = Field(..., description="Type of incident")
    history_score: float = Field(..., ge=0, le=100, description="Customer history score")

class ClaimScoreResponse(BaseModel):
    decision_id: UUID
    claim_id: str
    customer_id: str
    risk_score: float
    fraud_probability: float
    decision: str
    explanation: str
    model_version: str
    policy_version: str
    timestamp: datetime

class DecisionDetail(BaseModel):
    decision: ClaimScoreResponse
    audit_events: list[dict]
