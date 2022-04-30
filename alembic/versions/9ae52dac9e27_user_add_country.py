"""user add country

Revision ID: 9ae52dac9e27
Revises: c6188dc05aa8
Create Date: 2022-04-30 18:35:16.253336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae52dac9e27'
down_revision = 'c6188dc05aa8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('country', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'country')
    # ### end Alembic commands ###
