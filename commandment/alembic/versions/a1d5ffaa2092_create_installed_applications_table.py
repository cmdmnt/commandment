"""Create installed_applications table

Revision ID: a1d5ffaa2092
Revises: a35eeb5a216e
Create Date: 2017-05-19 19:43:10.092363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1d5ffaa2092'
down_revision = 'a35eeb5a216e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('installed_applications',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('device_udid', commandment.dbtypes.GUID(), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('bundle_identifier', sa.String(), nullable=True),
                    sa.Column('version', sa.String(), nullable=True),
                    sa.Column('short_version', sa.String(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('bundle_size', sa.BigInteger(), nullable=True),
                    sa.Column('dynamic_size', sa.BigInteger(), nullable=True),
                    sa.Column('is_validated', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_installed_applications_bundle_identifier'), 'installed_applications', ['bundle_identifier'], unique=False)
    op.create_index(op.f('ix_installed_applications_device_udid'), 'installed_applications', ['device_udid'], unique=False)
    op.create_index(op.f('ix_installed_applications_version'), 'installed_applications', ['version'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_installed_applications_version'), table_name='installed_applications')
    op.drop_index(op.f('ix_installed_applications_device_udid'), table_name='installed_applications')
    op.drop_index(op.f('ix_installed_applications_bundle_identifier'), table_name='installed_applications')
    op.drop_table('installed_applications')
