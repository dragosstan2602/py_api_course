"""Add content column

Revision ID: 11fb96de2d53
Revises: 867ef38782d2
Create Date: 2022-04-02 13:46:12.128991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11fb96de2d53'
down_revision = '867ef38782d2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False)
                  )
    pass


def downgrade():
    op.drop_column('posts',
                   'content'
                   )
