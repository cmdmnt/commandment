"""add dep profile relationships

Revision ID: 7cf5787a089e
Revises: b231394ab475
Create Date: 2018-11-06 21:11:54.606189

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '7cf5787a089e'
down_revision = 'b231394ab475'
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
    op.add_column('dep_accounts', sa.Column('default_dep_profile_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'dep_accounts', 'dep_profiles', ['default_dep_profile_id'], ['id'])
    op.add_column('dep_profiles', sa.Column('dep_account_id', sa.Integer(), nullable=True))
    op.add_column('dep_profiles', sa.Column('skip_setup_items', commandment.dbtypes.JSONEncodedDict(), nullable=True))
    op.create_foreign_key(None, 'dep_profiles', 'dep_accounts', ['dep_account_id'], ['id'])


def schema_downgrades():
    op.drop_constraint(None, 'dep_profiles', type_='foreignkey')
    op.drop_column('dep_profiles', 'skip_setup_items')
    op.drop_column('dep_profiles', 'dep_account_id')
    op.drop_constraint(None, 'dep_accounts', type_='foreignkey')
    op.drop_column('dep_accounts', 'default_dep_profile_id')
