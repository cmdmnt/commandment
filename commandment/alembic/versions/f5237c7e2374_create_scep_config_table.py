"""Create scep_config table

Revision ID: f5237c7e2374
Revises: e58afdc17baa
Create Date: 2017-05-19 19:34:00.120370

"""
from alembic import op, context
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f5237c7e2374'
down_revision = 'e58afdc17baa'
branch_labels = None
depends_on = None

TABLE = ('scep_config',
         sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
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

DEMO_SCEP_CONFIG = {
    'url': 'http://localhost:5000',
    'challenge_enabled': True,
    'challenge': 'sekret',
    'subject': 'CN=%HardwareUUID%',
    'key_size': 2048,
    'key_usage': 'All',
    'retries': 3,
    'retry_delay': 10,
    'certificate_renewal_time_interval': 24
}


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table(*TABLE)


def schema_downgrades():
    op.drop_table('scep_config')


def data_upgrades():
    tbl = sa.table(*TABLE[:-1])

    op.bulk_insert(tbl, [
        DEMO_SCEP_CONFIG
    ])


def data_downgrades():
    pass
