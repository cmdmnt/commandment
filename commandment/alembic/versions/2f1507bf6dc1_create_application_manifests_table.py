"""create application_manifests table

Revision ID: 2f1507bf6dc1
Revises: 7ab500f58a76
Create Date: 2017-10-15 17:37:04.645717

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '2f1507bf6dc1'
down_revision = '7ab500f58a76'
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
    op.create_table(
        'application_manifests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('bundle_id', sa.String()),
        sa.Column('bundle_version', sa.String()),
        sa.Column('kind', sa.String()),
        sa.Column('size_in_bytes', sa.BigInteger()),
        sa.Column('subtitle', sa.String()),
        sa.Column('title', sa.String()),
        sa.Column('display_image_url', sa.String()),
        sa.Column('display_image_needs_shine', sa.Boolean()),
        sa.Column('full_image_url', sa.String()),
        sa.Column('full_image_needs_shine', sa.Boolean()),
        sa.UniqueConstraint('bundle_id', 'bundle_version', name='uq_application_bundle_version')
    )

    op.create_table(
        'application_manifest_checksums',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('application_manifest_id', sa.Integer(), nullable=False),
        sa.Column('checksum_index', sa.Integer(), nullable=False),
        sa.Column('checksum_value', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['application_manifest_id'], ['application_manifests.id'], ondelete="CASCADE"),
        sa.UniqueConstraint('application_manifest_id', 'checksum_index', name='uq_application_checksum_index')
    )


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table('application_manifest_checksums')
    op.drop_table('application_manifests')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
