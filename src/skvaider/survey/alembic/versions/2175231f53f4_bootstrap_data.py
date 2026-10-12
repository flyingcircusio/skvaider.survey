"""bootstrap data

Revision ID: 2175231f53f4
Revises: db2af1aa7bbf
Create Date: 2026-10-12 14:45:54.246628

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2175231f53f4"
down_revision: str | Sequence[str] | None = "db2af1aa7bbf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        sa.text("""
        INSERT INTO
        models
        (id, name, value) VALUES
        (1, 'one', 'the one')
        """)
    )


def downgrade() -> None:
    """Downgrade schema."""
