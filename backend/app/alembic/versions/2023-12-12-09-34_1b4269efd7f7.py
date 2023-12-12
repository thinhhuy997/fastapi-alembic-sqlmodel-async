"""empty message

Revision ID: 1b4269efd7f7
Revises: 4de89458b576
Create Date: 2023-12-12 09:34:39.896448

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = '1b4269efd7f7'
down_revision = '4de89458b576'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm") 
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Album',
    sa.Column('album_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('artist', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Album_album_name'), 'Album', ['album_name'], unique=False)
    op.create_index(op.f('ix_Album_id'), 'Album', ['id'], unique=False)
    op.create_table('Track',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Track_id'), 'Track', ['id'], unique=False)
    op.create_index(op.f('ix_Track_title'), 'Track', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Track_title'), table_name='Track')
    op.drop_index(op.f('ix_Track_id'), table_name='Track')
    op.drop_table('Track')
    op.drop_index(op.f('ix_Album_id'), table_name='Album')
    op.drop_index(op.f('ix_Album_album_name'), table_name='Album')
    op.drop_table('Album')
    # ### end Alembic commands ###
