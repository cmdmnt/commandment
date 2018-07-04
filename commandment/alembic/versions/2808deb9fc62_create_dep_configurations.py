"""Create DEP configurations

Revision ID: 2808deb9fc62
Revises: 0201b96ab856
Create Date: 2018-07-04 16:57:16.899029

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '2808deb9fc62'
down_revision = '0201b96ab856'
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
    op.create_table('dep_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('certificate_id', sa.Integer(), nullable=True),
        sa.Column('consumer_key', sa.String(), nullable=True),
        sa.Column('consumer_secret', sa.String(), nullable=True),
        sa.Column('access_token', sa.String(), nullable=True),
        sa.Column('access_secret', sa.String(), nullable=True),
        sa.Column('access_token_expiry', sa.DateTime(), nullable=True),
        sa.Column('token_updated_at', sa.DateTime(), nullable=True),
        sa.Column('auth_session_token', sa.String(), nullable=True),
        sa.Column('server_name', sa.String(), nullable=True),
        sa.Column('server_uuid', commandment.dbtypes.GUID(), nullable=True),
        sa.Column('admin_id', sa.String(), nullable=True),
        sa.Column('facilitator_id', sa.String(), nullable=True),
        sa.Column('org_name', sa.String(), nullable=True),
        sa.Column('org_email', sa.String(), nullable=True),
        sa.Column('org_phone', sa.String(), nullable=True),
        sa.Column('org_address', sa.String(), nullable=True),
        sa.Column('org_type', sa.Enum('Education', 'Organization', name='deporgtype'), nullable=True),
        sa.Column('org_version', sa.Enum('v1', 'v2', name='deporgversion'), nullable=True),
        sa.Column('org_id', sa.String(), nullable=True),
        sa.Column('org_id_hash', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('cursor', sa.String(), nullable=True),
        sa.Column('more_to_follow', sa.Boolean(), nullable=True),
        sa.Column('fetched_until', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def schema_downgrades():
    op.drop_table('dep_accounts')



# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#     pass
#
#
# def data_downgrades():
#     """Add any optional data downgrade migrations here!"""
#     pass
