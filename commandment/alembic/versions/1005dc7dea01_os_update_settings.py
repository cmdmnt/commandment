"""os_update_settings

Revision ID: 1005dc7dea01
Revises: b74ca08cfd9a
Create Date: 2018-02-02 15:49:22.170956

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '1005dc7dea01'
down_revision = 'b74ca08cfd9a'
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
    """schema upgrade migrations go here."""
    op.add_column('devices', sa.Column('osu_automatic_app_installation_enabled', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_automatic_check_enabled', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_automatic_os_installation_enabled', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_automatic_security_updates_enabled', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_background_download_enabled', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_catalog_url', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('osu_is_default_catalog', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_perform_periodic_check', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('osu_previous_scan_date', sa.DateTime(), nullable=True))
    op.add_column('devices', sa.Column('osu_previous_scan_result', sa.String(), nullable=True))


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_column('devices', 'osu_previous_scan_result')
    op.drop_column('devices', 'osu_previous_scan_date')
    op.drop_column('devices', 'osu_perform_periodic_check')
    op.drop_column('devices', 'osu_is_default_catalog')
    op.drop_column('devices', 'osu_catalog_url')
    op.drop_column('devices', 'osu_background_download_enabled')
    op.drop_column('devices', 'osu_automatic_security_updates_enabled')
    op.drop_column('devices', 'osu_automatic_os_installation_enabled')
    op.drop_column('devices', 'osu_automatic_check_enabled')
    op.drop_column('devices', 'osu_automatic_app_installation_enabled')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
