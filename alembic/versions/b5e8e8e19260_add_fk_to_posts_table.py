"""add FK to posts table

Revision ID: b5e8e8e19260
Revises: b75803f9138a
Create Date: 2022-04-02 14:09:28.692173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5e8e8e19260'
down_revision = 'b75803f9138a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False)
                  )
    
    op.create_foreign_key('posts_users_fk', 
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', 
                       table_name='posts'
                       )
    
    op.drop_column('posts',
                   'owner_id'
                   )
    pass
