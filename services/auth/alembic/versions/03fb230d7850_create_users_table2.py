"""create users table2

Revision ID: 03fb230d7850
Revises: c6b43ba56978
Create Date: 2025-11-30 20:11:33.742365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03fb230d7850'
down_revision: Union[str, Sequence[str], None] = 'c6b43ba56978'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
