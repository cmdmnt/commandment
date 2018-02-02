"""create installed_payloads

Revision ID: 7ab500f58a76
Revises: f029ac1af3f0
Create Date: 2017-07-19 14:17:49.094292

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '7ab500f58a76'
down_revision = 'f029ac1af3f0'
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
    op.create_table('installed_payloads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('organization', sa.String(), nullable=True),
    sa.Column('payload_type', sa.String(), nullable=True),
    sa.Column('uuid', commandment.dbtypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(['profile_id'], ['installed_profiles.id'], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint('id')
    )


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table('installed_payloads')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
