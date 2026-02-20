import uuid
from sqlalchemy import Column, String, Float, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.database import Base

class Decision(Base):
    __tablename__ = "decisions"
    
    decision_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(Text, nullable=False, index=True)
    customer_id = Column(Text, nullable=False, index=True)
    model_version = Column(Text, nullable=False, default="rb-v1")
    policy_version = Column(Text, nullable=False, default="policy-v1")
    risk_score = Column(Float, nullable=False)
    fraud_probability = Column(Float, nullable=False)
    decision = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id = Column(UUID(as_uuid=True), ForeignKey("decisions.decision_id"), nullable=False)
    event_type = Column(Text, nullable=False)
    event_payload = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
