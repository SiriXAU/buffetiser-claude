"""Change dividend_reinvestment units to float

Revision ID: 001
Revises:
Create Date: 2025-01-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Change dividend_reinvestments.units from Integer to Float
    to support fractional share reinvestments (DRP).
    """
    # SQLite doesn't support ALTER COLUMN directly, but since PostgreSQL is used:
    op.alter_column(
        'dividend_reinvestments',
        'units',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False,
        nullable=False
    )


def downgrade() -> None:
    """
    Revert dividend_reinvestments.units back to Integer.
    Warning: This will truncate any fractional values!
    """
    op.alter_column(
        'dividend_reinvestments',
        'units',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False,
        nullable=False
    )
