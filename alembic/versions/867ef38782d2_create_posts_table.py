"""Create posts table

Revision ID: 867ef38782d2
Revises: 
Create Date: 2022-04-01 18:36:29.290796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867ef38782d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
