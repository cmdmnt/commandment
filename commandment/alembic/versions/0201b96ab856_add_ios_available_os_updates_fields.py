"""add ios available os updates fields

Revision ID: 0201b96ab856
Revises: e947cdf82307
Create Date: 2018-07-01 21:37:27.355712

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '0201b96ab856'
down_revision = 'e947cdf82307'
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
    op.add_column('available_os_updates', sa.Column('build', sa.String(), nullable=True))
    op.add_column('available_os_updates', sa.Column('download_size', sa.BigInteger(), nullable=True))
    op.add_column('available_os_updates', sa.Column('install_size', sa.BigInteger(), nullable=True))
    op.add_column('available_os_updates', sa.Column('product_name', sa.String(), nullable=True))


def schema_downgrades():
    op.drop_column('available_os_updates', 'product_name')
    op.drop_column('available_os_updates', 'install_size')
    op.drop_column('available_os_updates', 'download_size')
    op.drop_column('available_os_updates', 'build')


# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#     pass
#
#
# def data_downgrades():
#     """Add any optional data downgrade migrations here!"""
#     pass
