"""Add outlook_event_id column to appointment table

Revision ID: add_outlook_event_id
Revises: c77b6fff5608
Create Date: 2025-07-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_outlook_event_id'
down_revision = 'c77b6fff5608'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('appointment', sa.Column('outlook_event_id', sa.String(), nullable=True))


def downgrade():
    op.drop_column('appointment', 'outlook_event_id')
