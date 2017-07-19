"""Create dep_profiles table

Revision ID: a2e0af380181
Revises: 6675e981817e
Create Date: 2017-07-19 12:50:41.318647

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

from alembic import context

# revision identifiers, used by Alembic.
revision = 'a2e0af380181'
down_revision = '6675e981817e'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    op.create_table('dep_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', commandment.dbtypes.GUID(), nullable=True),
    sa.Column('profile_name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('allow_pairing', sa.Boolean(), nullable=True),
    sa.Column('is_supervised', sa.Boolean(), nullable=True),
    sa.Column('is_multi_user', sa.Boolean(), nullable=True),
    sa.Column('is_mandatory', sa.Boolean(), nullable=True),
    sa.Column('await_device_configured', sa.Boolean(), nullable=True),
    sa.Column('is_mdm_removable', sa.Boolean(), nullable=True),
    sa.Column('support_phone_number', sa.String(), nullable=True),
    sa.Column('auto_advance_setup', sa.Boolean(), nullable=True),
    sa.Column('support_email_address', sa.String(), nullable=True),
    sa.Column('org_magic', sa.String(), nullable=True),
    sa.Column('department', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dep_profiles_uuid'), 'dep_profiles', ['uuid'], unique=False)


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_index(op.f('ix_dep_profiles_uuid'), table_name='dep_profiles')
    op.drop_table('dep_profiles')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
