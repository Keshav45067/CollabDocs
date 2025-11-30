"""create users tableFinal

Revision ID: 3503e3e12cb0
Revises: 390efb67479c
Create Date: 2025-11-30 20:15:16.458780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3503e3e12cb0'
down_revision: Union[str, Sequence[str], None] = '390efb67479c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
