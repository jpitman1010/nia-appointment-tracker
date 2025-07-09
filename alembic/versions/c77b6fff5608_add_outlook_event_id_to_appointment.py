"""Add outlook_event_id to appointment

Revision ID: c77b6fff5608
Revises: e1b1d33795de
Create Date: 2025-07-08 12:11:16.708682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'c77b6fff5608'
down_revision: Union[str, None] = 'e1b1d33795de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('appointment', sa.Column('outlook_event_id', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('appointment', 'outlook_event_id')