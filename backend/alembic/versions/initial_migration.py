"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-04-10 00:45:55.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create threats table
    op.create_table(
        'threats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('threat_type', sa.String(), nullable=True),
        sa.Column('severity', sa.Float(), nullable=True),
        sa.Column('source_ip', sa.String(), nullable=True),
        sa.Column('destination_ip', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('raw_data', JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threats_threat_type'), 'threats', ['threat_type'], unique=False)
    op.create_index(op.f('ix_threats_source_ip'), 'threats', ['source_ip'], unique=False)
    op.create_index(op.f('ix_threats_status'), 'threats', ['status'], unique=False)

    # Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('threat_id', sa.Integer(), nullable=True),
        sa.Column('alert_type', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('metadata', JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['threat_id'], ['threats.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_alert_type'), 'alerts', ['alert_type'], unique=False)
    op.create_index(op.f('ix_alerts_status'), 'alerts', ['status'], unique=False)

def downgrade() -> None:
    op.drop_table('alerts')
    op.drop_table('threats')
