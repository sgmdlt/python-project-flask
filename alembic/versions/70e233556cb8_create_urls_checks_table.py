"""create urls_checks table

Revision ID: 70e233556cb8
Revises: 4307c25b1ee5
Create Date: 2022-08-23 19:30:07.469497

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '70e233556cb8'
down_revision = '4307c25b1ee5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'urls_checks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url_id', sa.Integer, sa.ForeignKey('urls.id', ondelete='CASCADE', onupdate='CASCADE')),  # noqa: E501
        sa.Column('status_code', sa.Integer),
        sa.Column('h1', sa.String(255)),
        sa.Column('title', sa.String(255)),
        sa.Column('description', sa.String(255)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),  # noqa: E501
    )


def downgrade() -> None:
    op.drop_table('urls_checks')
