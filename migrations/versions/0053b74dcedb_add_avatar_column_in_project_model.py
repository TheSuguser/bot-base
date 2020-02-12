"""add avatar column in Project model

Revision ID: 0053b74dcedb
Revises: 23bc4aa0a0f4
Create Date: 2020-02-05 13:41:23.883557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0053b74dcedb'
down_revision = '23bc4aa0a0f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('bot_avatar', sa.String(length=200), nullable=True))
    op.add_column('project', sa.Column('user_avatar', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'user_avatar')
    op.drop_column('project', 'bot_avatar')
    # ### end Alembic commands ###