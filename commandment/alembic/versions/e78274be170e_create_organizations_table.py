"""Create organizations table

Revision ID: e78274be170e
Revises: e9b0a4f7b595
Create Date: 2017-05-19 19:28:42.596244

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table
from alembic import context

# revision identifiers, used by Alembic.
revision = 'e78274be170e'
down_revision = 'e9b0a4f7b595'
branch_labels = None
depends_on = None

TABLE = (
    'organizations',
    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('payload_prefix', sa.String(), nullable=True),
    sa.Column('x509_ou', sa.String(length=32), nullable=True),
    sa.Column('x509_o', sa.String(length=64), nullable=True),
    sa.Column('x509_st', sa.String(length=128), nullable=True),
    sa.Column('x509_c', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
)

DEMO_ORGANIZATION = {
    'name': 'Commandment Inc',
    'payload_prefix': 'dev.commandment',
    'x509_c': 'US',
    'x509_o': 'Commandment',
    'x509_ou': 'MDM'
}


def upgrade():
    schema_upgrades()
    # if context.get_x_argument(as_dictionary=True).get('data', None):
    #     data_upgrades()


def downgrade():
    # if context.get_x_argument(as_dictionary=True).get('data', None):
    #     data_downgrades()
    schema_downgrades()


def schema_upgrades():
    op.create_table(*TABLE)


def schema_downgrades():
    op.drop_table('organizations')


def data_upgrades():
    tbl = table(*TABLE[:-1])

    op.bulk_insert(tbl, [
        DEMO_ORGANIZATION
    ])


def data_downgrades():
    pass
