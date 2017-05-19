"""Create devices table

Revision ID: 50188ffaf0cd
Revises: 71ecf957301a
Create Date: 2017-05-19 19:39:22.021264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50188ffaf0cd'
down_revision = '71ecf957301a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('devices',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('udid', sa.String(), nullable=True),
                    sa.Column('topic', sa.String(), nullable=True),
                    sa.Column('last_seen', sa.DateTime(), nullable=True),
                    sa.Column('is_enrolled', sa.Boolean(), nullable=True),
                    sa.Column('build_version', sa.String(), nullable=True),
                    sa.Column('device_name', sa.String(), nullable=True),
                    sa.Column('model', sa.String(), nullable=True),
                    sa.Column('model_name', sa.String(), nullable=True),
                    sa.Column('os_version', sa.String(), nullable=True),
                    sa.Column('product_name', sa.String(), nullable=True),
                    sa.Column('serial_number', sa.String(length=64), nullable=True),
                    sa.Column('hostname', sa.String(), nullable=True),
                    sa.Column('local_hostname', sa.String(), nullable=True),
                    sa.Column('available_device_capacity', sa.Float(), nullable=True),
                    sa.Column('device_capacity', sa.Float(), nullable=True),
                    sa.Column('wifi_mac', sa.String(), nullable=True),
                    sa.Column('bluetooth_mac', sa.String(), nullable=True),
                    sa.Column('awaiting_configuration', sa.Boolean(), nullable=True),
                    sa.Column('push_magic', sa.String(), nullable=True),
                    sa.Column('_token', sa.String(), nullable=True),
                    sa.Column('tokenupdate_at', sa.DateTime(), nullable=True),
                    sa.Column('last_push_at', sa.DateTime(), nullable=True),
                    sa.Column('last_apns_id', sa.Integer(), nullable=True),
                    sa.Column('failed_push_count', sa.Integer(), nullable=False),
                    sa.Column('unlock_token', sa.String(), nullable=True),
                    sa.Column('passcode_present', sa.Boolean(), nullable=True),
                    sa.Column('passcode_compliant', sa.Boolean(), nullable=True),
                    sa.Column('passcode_compliant_with_profiles', sa.Boolean(), nullable=True),
                    sa.Column('fde_enabled', sa.Boolean(), nullable=True),
                    sa.Column('fde_has_prk', sa.Boolean(), nullable=True),
                    sa.Column('fde_has_irk', sa.Boolean(), nullable=True),
                    sa.Column('firewall_enabled', sa.Boolean(), nullable=True),
                    sa.Column('block_all_incoming', sa.Boolean(), nullable=True),
                    sa.Column('stealth_mode_enabled', sa.Boolean(), nullable=True),
                    sa.Column('sip_enabled', sa.Boolean(), nullable=True),
                    sa.Column('certificate_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_devices_serial_number'), 'devices', ['serial_number'], unique=False)
    op.create_index(op.f('ix_devices_udid'), 'devices', ['udid'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_devices_udid'), table_name='devices')
    op.drop_index(op.f('ix_devices_serial_number'), table_name='devices')
    op.drop_table('devices')
