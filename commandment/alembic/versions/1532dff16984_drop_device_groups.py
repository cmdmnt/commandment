"""drop device groups

Revision ID: 1532dff16984
Revises: f8eb70b3aa2b
Create Date: 2018-03-13 21:26:13.058020

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

from alembic import context

# revision identifiers, used by Alembic.
revision = '1532dff16984'
down_revision = 'f8eb70b3aa2b'
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
    op.drop_table('device_groups')
    op.drop_table('device_group_devices')


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.create_table('device_group_devices',
                    sa.Column('device_group_id', sa.INTEGER(), nullable=False),
                    sa.Column('device_id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['device_group_id'], ['device_groups.id'], ),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.PrimaryKeyConstraint('device_group_id', 'device_id')
                    )
    op.create_table('device_groups',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
