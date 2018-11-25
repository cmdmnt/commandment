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
    with op.batch_alter_table('dep_accounts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('default_dep_profile_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_dep_accounts_default_dep_profile_id', 'dep_profiles', ['default_dep_profile_id'], ['id'])

    with op.batch_alter_table('dep_profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dep_account_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('skip_setup_items', commandment.dbtypes.JSONEncodedDict(), nullable=True))
        batch_op.create_foreign_key('fk_dep_profiles_dep_account_id', 'dep_accounts', ['dep_account_id'], ['id'])


def schema_downgrades():
    with op.batch_alter_table('dep_profiles', schema=None) as batch_op:
        batch_op.drop_constraint('fk_dep_profiles_dep_account_id', 'dep_profiles', type_='foreignkey')
        batch_op.drop_column('skip_setup_items')
        batch_op.drop_column('dep_account_id')

    with op.batch_alter_table('dep_accounts', schema=None) as batch_op:
        batch_op.drop_constraint('fk_dep_accounts_default_dep_profile_id', 'dep_accounts', type_='foreignkey')
        batch_op.drop_column('default_dep_profile_id')
