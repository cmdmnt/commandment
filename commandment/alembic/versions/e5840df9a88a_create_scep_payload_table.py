"""Create scep_payload table

Revision ID: e5840df9a88a
Revises: fc0c134cbb2e
Create Date: 2017-05-19 19:58:54.048729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5840df9a88a'
down_revision = 'fc0c134cbb2e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('scep_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('subject', commandment.dbtypes.JSONEncodedDict(), nullable=False),
                    sa.Column('challenge', sa.String(), nullable=True),
                    sa.Column('key_size', sa.Integer(), nullable=False),
                    sa.Column('ca_fingerprint', sa.LargeBinary(), nullable=True),
                    sa.Column('key_type', sa.String(), nullable=False),
                    sa.Column('key_usage', sa.Enum('Signing', 'Encryption', 'All', name='keyusage'), nullable=True),
                    sa.Column('subject_alt_name', sa.String(), nullable=True),
                    sa.Column('retries', sa.Integer(), nullable=False),
                    sa.Column('retry_delay', sa.Integer(), nullable=False),
                    sa.Column('certificate_renewal_time_interval', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('scep_payload')
