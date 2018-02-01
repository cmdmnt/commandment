"""Create application_sources table

Revision ID: 71818e983100
Revises: da52b64b865f
Create Date: 2017-05-18 22:29:40.036227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71818e983100'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('application_sources',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('source_type', sa.Enum('S3', 'Munki', name='appsourcetype'), nullable=True),
                    sa.Column('endpoint', sa.String(), nullable=True),
                    sa.Column('mount_uri', sa.String(), nullable=True),
                    sa.Column('use_ssl', sa.Boolean(), nullable=True),
                    sa.Column('access_key', sa.String(), nullable=True),
                    sa.Column('secret_key', sa.String(), nullable=True),
                    sa.Column('bucket', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('application_sources')
