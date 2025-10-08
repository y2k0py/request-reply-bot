"""add CHANNEL_ID to tagsenums

Revision ID: c0cc0a72f6ec
Revises: f26567f717a8
Create Date: 2025-10-08 23:51:46.610457
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "c0cc0a72f6ec"
down_revision = "f26567f717a8"
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE tagsenums ADD VALUE IF NOT EXISTS 'CHANNEL_ID'")


def downgrade():
    pass
