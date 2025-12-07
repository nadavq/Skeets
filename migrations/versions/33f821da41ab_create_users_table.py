"""Create users table

Revision ID: 33f821da41ab
Revises: 
Create Date: 2025-11-15 12:58:14.526761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '33f821da41ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    import datetime
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("creation_time", sa.DateTime(), nullable=False, default=datetime.datetime.now),
        sa.Column("last_update_time", sa.DateTime(), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("last_name", sa.String(255), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("users")
