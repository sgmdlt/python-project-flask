"""create urls table

Revision ID: 4307c25b1ee5
Revises:
Create Date: 2022-08-23 19:11:53.599005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4307c25b1ee5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),  # noqa: E501
    )


def downgrade() -> None:
    op.drop_table('urls')
