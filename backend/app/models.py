import uuid
from sqlalchemy import Column, String, Float, Text, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import TypeDecorator
from app.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type - always uses String(36) for compatibility."""
    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, uuid.UUID):
                return str(value)
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if isinstance(value, uuid.UUID):
                return value
            return uuid.UUID(str(value))
        return value


class Decision(Base):
    __tablename__ = "decisions"
    
    decision_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
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
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    decision_id = Column(GUID(), ForeignKey("decisions.decision_id"), nullable=False)
    event_type = Column(Text, nullable=False)
    event_payload = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
