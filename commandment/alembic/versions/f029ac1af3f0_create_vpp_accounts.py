"""Create vpp_accounts table

Revision ID: f029ac1af3f0
Revises: 8c866896f76e
Create Date: 2017-07-19 13:02:13.563903

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'f029ac1af3f0'
down_revision = '8c866896f76e'
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
    op.create_table('vpp_accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stoken', sa.String(), nullable=False),
    sa.Column('licenses_since_modified_token', sa.String(), nullable=True),
    sa.Column('licenses_batch_token', sa.String(), nullable=True),
    sa.Column('users_since_modified_token', sa.String(), nullable=True),
    sa.Column('users_batch_token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table('vpp_accounts')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
