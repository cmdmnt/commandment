"""add ios installed application fields

Revision ID: e947cdf82307
Revises: 3061e56045eb
Create Date: 2018-07-01 20:30:53.621855

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'e947cdf82307'
down_revision = '3061e56045eb'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    # if context.get_x_argument(as_dictionary=True).get('data', None):
    #     data_upgrades()


def downgrade():
    # if context.get_x_argument(as_dictionary=True).get('data', None):
    #     data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.add_column('installed_applications', sa.Column('adhoc_codesigned', sa.Boolean(), nullable=True))
    op.add_column('installed_applications', sa.Column('appstore_vendable', sa.Boolean(), nullable=True))
    op.add_column('installed_applications', sa.Column('beta_app', sa.Boolean(), nullable=True))
    op.add_column('installed_applications', sa.Column('device_based_vpp', sa.Boolean(), nullable=True))
    op.add_column('installed_applications', sa.Column('has_update_available', sa.Boolean(), nullable=True))
    op.add_column('installed_applications', sa.Column('installing', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_installed_applications_external_version_identifier'), 'installed_applications',
                    ['external_version_identifier'], unique=False)


def schema_downgrades():
    op.drop_index(op.f('ix_installed_applications_external_version_identifier'), table_name='installed_applications')
    op.drop_column('installed_applications', 'installing')
    op.drop_column('installed_applications', 'has_update_available')
    op.drop_column('installed_applications', 'device_based_vpp')
    op.drop_column('installed_applications', 'beta_app')
    op.drop_column('installed_applications', 'appstore_vendable')
    op.drop_column('installed_applications', 'adhoc_codesigned')


# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#     pass
#
#
# def data_downgrades():
#     """Add any optional data downgrade migrations here!"""
#     pass
