"""Add DEP device columns

Revision ID: a3ddaad5c358
Revises: 2808deb9fc62
Create Date: 2018-07-04 21:44:41.549806

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'a3ddaad5c358'
down_revision = '2808deb9fc62'
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
    op.add_column('devices', sa.Column('description', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('asset_tag', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('color', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('device_assigned_by', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('device_assigned_date', sa.DateTime(), nullable=True))
    op.add_column('devices', sa.Column('device_family', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('is_dep', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('os', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('profile_assign_time', sa.DateTime(), nullable=True))
    op.add_column('devices', sa.Column('profile_push_time', sa.DateTime(), nullable=True))
    op.add_column('devices', sa.Column('profile_status', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('profile_uuid', sa.String(), nullable=True))
    op.create_foreign_key(None, 'devices', 'dep_profiles', ['dep_profile_id'], ['id'])


def schema_downgrades():
    op.drop_constraint(None, 'devices', type_='foreignkey')
    op.drop_column('devices', 'profile_uuid')
    op.drop_column('devices', 'profile_status')
    op.drop_column('devices', 'profile_push_time')
    op.drop_column('devices', 'profile_assign_time')
    op.drop_column('devices', 'os')
    op.drop_column('devices', 'is_dep')
    op.drop_column('devices', 'device_family')
    op.drop_column('devices', 'device_assigned_date')
    op.drop_column('devices', 'device_assigned_by')
    op.drop_column('devices', 'color')
    op.drop_column('devices', 'asset_tag')
    op.drop_column('devices', 'description')


# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#     pass
#
#
# def data_downgrades():
#     """Add any optional data downgrade migrations here!"""
#     pass
