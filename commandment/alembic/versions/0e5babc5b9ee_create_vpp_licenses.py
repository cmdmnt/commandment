"""Create vpp_licenses table

Revision ID: 0e5babc5b9ee
Revises: 875dcce0bf8b
Create Date: 2017-07-19 12:56:55.273155

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '0e5babc5b9ee'
down_revision = '875dcce0bf8b'
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
    op.create_table('vpp_licenses',
    sa.Column('license_id', sa.Integer(), nullable=False),
    sa.Column('adam_id', sa.String(), nullable=True),
    sa.Column('product_type', sa.Enum('Software', 'Application', 'Publication', name='vppproducttype'), nullable=True),
    sa.Column('product_type_name', sa.String(), nullable=True),
    sa.Column('pricing_param', sa.Enum('StandardQuality', 'HighQuality', name='vpppricingparam'), nullable=True),
    sa.Column('is_irrevocable', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('client_user_id', commandment.dbtypes.GUID(), nullable=True),
    sa.Column('its_id_hash', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['client_user_id'], ['vpp_users.client_user_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['vpp_users.user_id'], ),
    sa.PrimaryKeyConstraint('license_id')
    )


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table('vpp_licenses')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
