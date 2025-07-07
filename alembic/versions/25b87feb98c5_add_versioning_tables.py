"""Add versioning tables

Revision ID: 25b87feb98c5
Revises: 876ada1921e0
Create Date: 2025-07-07 11:46:04.779919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '25b87feb98c5'
down_revision: Union[str, None] = '876ada1921e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alembic autogenerate will handle the creation of versioning tables
    pass


def downgrade() -> None:
    # If needed, write SQL commands here to drop versioning tables,
    # or leave empty if you prefer not to support downgrading this migration
    pass
