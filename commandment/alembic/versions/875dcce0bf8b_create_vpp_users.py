"""Create vpp_users table

Revision ID: 875dcce0bf8b
Revises: a2e0af380181
Create Date: 2017-07-19 12:56:02.203987

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '875dcce0bf8b'
down_revision = 'a2e0af380181'
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
    op.create_table('vpp_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('client_user_id', commandment.dbtypes.GUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('Registered', 'Associated', 'Retired', 'Deleted', name='vppuserstatus'), nullable=True),
    sa.Column('invite_url', sa.String(), nullable=True),
    sa.Column('invite_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table('vpp_users')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
