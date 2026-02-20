"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-02-20 18:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'decisions',
        sa.Column('decision_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('claim_id', sa.Text(), nullable=False),
        sa.Column('customer_id', sa.Text(), nullable=False),
        sa.Column('model_version', sa.Text(), nullable=False),
        sa.Column('policy_version', sa.Text(), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('fraud_probability', sa.Float(), nullable=False),
        sa.Column('decision', sa.Text(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('decision_id')
    )
    op.create_index('ix_decisions_claim_id', 'decisions', ['claim_id'])
    op.create_index('ix_decisions_customer_id', 'decisions', ['customer_id'])
    
    op.create_table(
        'audit_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('decision_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.Text(), nullable=False),
        sa.Column('event_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['decision_id'], ['decisions.decision_id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('decisions')
