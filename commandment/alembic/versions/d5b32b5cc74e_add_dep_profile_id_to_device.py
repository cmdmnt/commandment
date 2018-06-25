"""add dep profile id to device

Revision ID: d5b32b5cc74e
Revises: 1005dc7dea01
Create Date: 2018-03-13 21:16:23.964086

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'd5b32b5cc74e'
down_revision = '1005dc7dea01'
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
    op.add_column('devices', sa.Column('dep_profile_id', sa.Integer(), nullable=True))
    # Unsupported on SQLite3
    # op.create_foreign_key(None, 'devices', 'dep_profiles', ['dep_profile_id'], ['id'])


def schema_downgrades():
    """schema downgrade migrations go here."""
    # Unsupported on SQLite3
    # op.drop_constraint(None, 'devices', type_='foreignkey')
    op.drop_column('devices', 'dep_profile_id')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
