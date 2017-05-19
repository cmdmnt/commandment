"""Create scep_config table

Revision ID: f5237c7e2374
Revises: e58afdc17baa
Create Date: 2017-05-19 19:34:00.120370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5237c7e2374'
down_revision = 'e58afdc17baa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('scep_config',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('challenge_enabled', sa.Boolean(), nullable=True),
                    sa.Column('challenge', sa.String(), nullable=True),
                    sa.Column('ca_fingerprint', sa.String(), nullable=True),
                    sa.Column('subject', sa.String(), nullable=False),
                    sa.Column('key_size', sa.Integer(), nullable=False),
                    sa.Column('key_type', sa.String(), nullable=False),
                    sa.Column('key_usage', sa.Enum('Signing', 'Encryption', 'All', name='keyusage'), nullable=True),
                    sa.Column('retries', sa.Integer(), nullable=False),
                    sa.Column('retry_delay', sa.Integer(), nullable=False),
                    sa.Column('certificate_renewal_time_interval', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('scep_config')
