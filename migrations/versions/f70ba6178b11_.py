"""empty message

Revision ID: f70ba6178b11
Revises: 29033582c021
Create Date: 2016-07-17 21:25:19.324669

"""

# revision identifiers, used by Alembic.
revision = 'f70ba6178b11'
down_revision = '29033582c021'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    ### end Alembic commands ###
