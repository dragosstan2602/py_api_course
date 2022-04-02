"""finished adding columns to posts

Revision ID: 470bb6fb32a7
Revises: b5e8e8e19260
Create Date: 2022-04-02 14:15:12.688464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '470bb6fb32a7'
down_revision = 'b5e8e8e19260'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')
                  )
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
                  )
    
    pass


def downgrade():
    op.drop_column('posts',
                   'published'
                   )

    op.drop_column('posts',
                   'created_at'
                   )