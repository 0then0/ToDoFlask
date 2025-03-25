"""Add created_at and updated_at to Task

Revision ID: 7f9bb57c66b9
Revises: 8024635ee6b4
Create Date: 2025-03-25 18:20:59.413524

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7f9bb57c66b9"
down_revision = "8024635ee6b4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "task",
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column(
        "task",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_column("task", "updated_at")
    op.drop_column("task", "created_at")
