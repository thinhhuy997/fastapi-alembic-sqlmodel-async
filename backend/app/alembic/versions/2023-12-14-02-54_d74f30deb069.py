"""empty message

Revision ID: d74f30deb069
Revises: 32fba1c85401
Create Date: 2023-12-14 02:54:38.484240

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel # added
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd74f30deb069'
down_revision = '32fba1c85401'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm") 
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Track_id', table_name='Track')
    op.drop_index('ix_Track_title', table_name='Track')
    op.drop_table('Track')
    op.drop_index('ix_member_age', table_name='member')
    op.drop_index('ix_member_name', table_name='member')
    op.drop_table('member')
    op.drop_index('ix_home_name', table_name='home')
    op.drop_table('home')
    op.drop_index('ix_Album_album_name', table_name='Album')
    op.drop_index('ix_Album_id', table_name='Album')
    op.drop_table('Album')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Album',
    sa.Column('album_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('artist', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['User.id'], name='Album_created_by_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Album_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_Album_id', 'Album', ['id'], unique=False)
    op.create_index('ix_Album_album_name', 'Album', ['album_name'], unique=False)
    op.create_table('home',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('home_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('headquarters', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='home_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_home_name', 'home', ['name'], unique=False)
    op.create_table('member',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('secret_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('home_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['home_id'], ['home.id'], name='member_home_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='member_pkey')
    )
    op.create_index('ix_member_name', 'member', ['name'], unique=False)
    op.create_index('ix_member_age', 'member', ['age'], unique=False)
    op.create_table('Track',
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('album_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['Album.id'], name='Track_album_id_fkey'),
    sa.ForeignKeyConstraint(['created_by_id'], ['User.id'], name='Track_created_by_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Track_pkey')
    )
    op.create_index('ix_Track_title', 'Track', ['title'], unique=False)
    op.create_index('ix_Track_id', 'Track', ['id'], unique=False)
    # ### end Alembic commands ###
