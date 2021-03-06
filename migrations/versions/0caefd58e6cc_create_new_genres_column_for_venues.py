"""create new genres column for venues

Revision ID: 0caefd58e6cc
Revises: a54ca80f1a00
Create Date: 2020-07-01 04:58:10.643178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0caefd58e6cc'
down_revision = 'a54ca80f1a00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('genres', sa.String(length=120), nullable=False))
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venues', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.drop_column('venues', 'genres')
    # ### end Alembic commands ###
