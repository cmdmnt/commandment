"""general cleanup

Revision ID: 3fb4a904979c
Revises: 1532dff16984
Create Date: 2018-03-13 21:27:55.983564

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

from alembic import context

# revision identifiers, used by Alembic.
revision = '3fb4a904979c'
down_revision = '1532dff16984'
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
    op.drop_table('users')
    op.drop_table('payload_dependencies')


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.create_table('payload_dependencies',
                    sa.Column('payload_uuid', sa.CHAR(length=32), nullable=True),
                    sa.Column('depends_on_payload_uuid', sa.CHAR(length=32), nullable=True),
                    sa.ForeignKeyConstraint(['depends_on_payload_uuid'], ['payloads.uuid'], ),
                    sa.ForeignKeyConstraint(['payload_uuid'], ['payloads.uuid'], )
                    )
    op.create_table('users',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(), nullable=True),
                    sa.Column('fullname', sa.VARCHAR(), nullable=True),
                    sa.Column('password', sa.VARCHAR(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('dep_configurations')
    op.drop_table('mdm_payload')
    op.drop_table('certificate_payload')
    op.drop_table('command_sequences')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
