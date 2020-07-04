"""add final new attributes.

Revision ID: 75563bca715f
Revises: 60d1642a0f4f
Create Date: 2020-07-02 07:26:07.116625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75563bca715f'
down_revision = '60d1642a0f4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.execute('UPDATE venues SET seeking_talent = True WHERE seeking_talent IS NULL')
    op.alter_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=False))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'seeking_description')
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###