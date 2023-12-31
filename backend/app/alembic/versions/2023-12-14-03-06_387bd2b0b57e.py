"""empty message

Revision ID: 387bd2b0b57e
Revises: bc403a224087
Create Date: 2023-12-14 03:06:21.179317

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = '387bd2b0b57e'
down_revision = 'bc403a224087'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm") 
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Track', 'duration',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_Track_duration'), 'Track', ['duration'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Track_duration'), table_name='Track')
    op.alter_column('Track', 'duration',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
