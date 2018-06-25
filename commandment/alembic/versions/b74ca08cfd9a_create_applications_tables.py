"""create applications tables

Revision ID: b74ca08cfd9a
Revises: 2f1507bf6dc1
Create Date: 2017-10-19 21:26:19.927682

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

from alembic import context

# revision identifiers, used by Alembic.
revision = 'b74ca08cfd9a'
down_revision = '2f1507bf6dc1'
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
    """schema upgrade migrations go here."""
    op.create_table('applications',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('display_name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('version', sa.String(), nullable=True),
                    sa.Column('itunes_store_id', sa.Integer(), nullable=True),
                    sa.Column('bundle_id', sa.String(), nullable=False),
                    sa.Column('purchase_method', sa.Integer(), nullable=True),
                    sa.Column('manifest_url', sa.String(), nullable=True),
                    sa.Column('management_flags', sa.Integer(), nullable=True),
                    sa.Column('change_management_state', sa.String(), nullable=True),
                    sa.Column('discriminator', sa.String(length=20), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_applications_bundle_id'), 'applications', ['bundle_id'], unique=False)
    op.create_index(op.f('ix_applications_discriminator'), 'applications', ['discriminator'], unique=False)



def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_index(op.f('ix_applications_discriminator'), table_name='applications')
    op.drop_index(op.f('ix_applications_bundle_id'), table_name='applications')
    op.drop_table('applications')
    # ### end Alembic commands ###


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
