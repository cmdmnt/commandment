"""create certificate authority

Revision ID: 3061e56045eb
Revises: 3fb4a904979c
Create Date: 2018-06-30 20:53:58.016051

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '3061e56045eb'
down_revision = '3fb4a904979c'
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
    op.create_table('certificate_authority',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('common_name', sa.String(), nullable=True),
    sa.Column('serial', sa.Integer(), nullable=True),
    sa.Column('validity_period', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.Column('rsa_private_key_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ),
    sa.ForeignKeyConstraint(['rsa_private_key_id'], ['rsa_private_keys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('common_name')
    )


def schema_downgrades():
    op.drop_table('certificate_authority')


# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#     pass
#
#
# def data_downgrades():
#     """Add any optional data downgrade migrations here!"""
#     pass
