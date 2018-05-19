"""create application manifests

Revision ID: f8eb70b3aa2b
Revises: d5b32b5cc74e
Create Date: 2018-03-13 21:21:31.277764

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'f8eb70b3aa2b'
down_revision = 'd5b32b5cc74e'
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
    # op.alter_column('application_manifest_checksums', 'application_manifest_id',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    #op.drop_constraint('uq_application_checksum_index', 'application_manifest_checksums', type_='unique')
    op.drop_constraint(None, 'application_manifest_checksums', type_='foreignkey')
    op.create_foreign_key(None, 'application_manifest_checksums', 'application_manifests', ['application_manifest_id'], ['id'])
    op.add_column('application_manifests', sa.Column('full_size_image_needs_shine', sa.Boolean(), nullable=True))
    op.add_column('application_manifests', sa.Column('full_size_image_url', sa.String(), nullable=True))
    op.alter_column('application_manifests', 'bundle_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_index(op.f('ix_application_manifests_bundle_id'), 'application_manifests', ['bundle_id'], unique=False)
    op.create_index(op.f('ix_application_manifests_bundle_version'), 'application_manifests', ['bundle_version'], unique=False)
    op.drop_constraint('uq_application_bundle_version', 'application_manifests', type_='unique')
    op.drop_column('application_manifests', 'full_image_url')
    op.drop_column('application_manifests', 'full_image_needs_shine')


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.add_column('application_manifests', sa.Column('full_image_needs_shine', sa.BOOLEAN(), nullable=True))
    op.add_column('application_manifests', sa.Column('full_image_url', sa.VARCHAR(), nullable=True))
    op.create_unique_constraint('uq_application_bundle_version', 'application_manifests', ['bundle_id', 'bundle_version'])
    op.drop_index(op.f('ix_application_manifests_bundle_version'), table_name='application_manifests')
    op.drop_index(op.f('ix_application_manifests_bundle_id'), table_name='application_manifests')
    op.alter_column('application_manifests', 'bundle_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('application_manifests', 'full_size_image_url')
    op.drop_column('application_manifests', 'full_size_image_needs_shine')
    op.drop_constraint(None, 'application_manifest_checksums', type_='foreignkey')
    op.create_foreign_key(None, 'application_manifest_checksums', 'application_manifests', ['application_manifest_id'], ['id'], ondelete='CASCADE')
    #op.create_unique_constraint('uq_application_checksum_index', 'application_manifest_checksums', ['application_manifest_id', 'checksum_index'])
    # op.alter_column('application_manifest_checksums', 'application_manifest_id',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
