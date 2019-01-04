"""Create installed_profiles table

Revision ID: a35eeb5a216e
Revises: e16577adc4fd
Create Date: 2017-05-19 19:41:46.995463

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = 'a35eeb5a216e'
down_revision = 'e16577adc4fd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('installed_profiles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('device_udid', sa.String(40), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('has_removal_password', sa.Boolean(), nullable=True),
                    sa.Column('is_encrypted', sa.Boolean(), nullable=True),
                    sa.Column('is_managed', sa.Boolean(), nullable=True),
                    sa.Column('payload_description', sa.String(), nullable=True),
                    sa.Column('payload_display_name', sa.String(), nullable=True),
                    sa.Column('payload_identifier', sa.String(), nullable=True),
                    sa.Column('payload_organization', sa.String(), nullable=True),
                    sa.Column('payload_removal_disallowed', sa.Boolean(), nullable=True),
                    sa.Column('payload_uuid', commandment.dbtypes.GUID(), nullable=True),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_installed_profiles_device_udid'), 'installed_profiles', ['device_udid'], unique=False)
    op.create_index(op.f('ix_installed_profiles_payload_uuid'), 'installed_profiles', ['payload_uuid'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_installed_profiles_payload_uuid'), table_name='installed_profiles')
    op.drop_index(op.f('ix_installed_profiles_device_udid'), table_name='installed_profiles')
    op.drop_table('installed_profiles')
