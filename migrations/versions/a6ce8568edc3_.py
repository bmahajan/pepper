"""empty message

Revision ID: a6ce8568edc3
Revises: 0ed2f485a3fe
Create Date: 2016-08-14 14:26:21.016738

"""

# revision identifiers, used by Alembic.
revision = 'a6ce8568edc3'
down_revision = '0ed2f485a3fe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_roles', sa.Column('role_name', sa.String(length=64), nullable=True))
    op.drop_column('user_roles', 'role_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_roles', sa.Column('role_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('user_roles', 'role_name')
    ### end Alembic commands ###
