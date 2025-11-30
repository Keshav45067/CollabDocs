"""create users table3

Revision ID: 390efb67479c
Revises: 03fb230d7850
Create Date: 2025-11-30 20:13:07.026035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '390efb67479c'
down_revision: Union[str, Sequence[str], None] = '03fb230d7850'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
