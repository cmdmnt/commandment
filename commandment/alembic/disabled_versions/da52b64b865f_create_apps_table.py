"""Create apps table

Revision ID: da52b64b865f
Revises:
Create Date: 2017-05-18 22:27:44.830159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da52b64b865f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('apps',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('filename', sa.String(), nullable=False),
                    sa.Column('filesize', sa.Integer(), nullable=False),
                    sa.Column('md5_hash', sa.String(length=32), nullable=False),
                    sa.Column('md5_chunk_size', sa.Integer(), nullable=False),
                    sa.Column('md5_chunk_hashes', sa.Text(), nullable=True),
                    sa.Column('bundle_ids_json', sa.Text(), nullable=True),
                    sa.Column('pkg_ids_json', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('filename')
                    )


def downgrade():
    op.drop_table('app')

