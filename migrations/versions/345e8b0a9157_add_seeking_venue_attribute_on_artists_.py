"""add seeking_venue attribute on artists table.

Revision ID: 345e8b0a9157
Revises: 49a77b910804
Create Date: 2020-07-02 05:06:18.224887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '345e8b0a9157'
down_revision = '49a77b910804'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.execute('UPDATE artists SET seeking_venue = True WHERE seeking_venue IS NULL')
    op.alter_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=False))
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###