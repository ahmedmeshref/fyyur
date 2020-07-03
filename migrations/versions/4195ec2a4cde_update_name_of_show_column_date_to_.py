"""update name of show column, date to start time.

Revision ID: 4195ec2a4cde
Revises: 0f9adcb9d8b1
Create Date: 2020-07-04 01:36:23.821595

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '4195ec2a4cde'
down_revision = '0f9adcb9d8b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.execute('UPDATE shows SET start_time = \'2020-01-16 00:00:00.000\' WHERE start_time IS NULL;')
    op.alter_column('shows', sa.Column('start_time', sa.DateTime(), nullable=False))
    op.drop_column('shows', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('shows', 'start_time')
    # ### end Alembic commands ###
