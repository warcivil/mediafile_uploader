"""rename audio to media file

Revision ID: 6b3c6ea62d98
Revises: 840a096ddbe1
Create Date: 2024-08-03 22:17:00.933126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b3c6ea62d98'
down_revision: Union[str, None] = '840a096ddbe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_file',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('uid', sa.UUID(), nullable=True),
    sa.Column('file_path', sa.String(), nullable=True),
    sa.Column('link_on_cloud', sa.String(), nullable=True),
    sa.Column('metadata_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['metadata_id'], ['metadata_media_file.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_media_file_uid'), 'media_file', ['uid'], unique=False)
    op.drop_index('ix_audio_uid', table_name='audio')
    op.drop_table('audio')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('file_path', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('link_on_cloud', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('metadata_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['metadata_id'], ['metadata_media_file.id'], name='audio_metadata_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='audio_pkey')
    )
    op.create_index('ix_audio_uid', 'audio', ['uid'], unique=False)
    op.drop_index(op.f('ix_media_file_uid'), table_name='media_file')
    op.drop_table('media_file')
    # ### end Alembic commands ###
