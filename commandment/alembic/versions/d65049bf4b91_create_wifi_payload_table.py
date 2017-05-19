"""Create wifi_payload table

Revision ID: d65049bf4b91
Revises: 9dd4e48235e3
Create Date: 2017-05-19 20:00:36.548840

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = 'd65049bf4b91'
down_revision = '9dd4e48235e3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('wifi_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('ssid_str', sa.String(), nullable=False),
                    sa.Column('hidden_network', sa.Boolean(), nullable=True),
                    sa.Column('auto_join', sa.Boolean(), nullable=True),
                    sa.Column('encryption_type', sa.Enum('ENone', 'Any', 'WPA2', 'WPA', 'WEP', name='wifiencryptiontype'), nullable=True),
                    sa.Column('is_hotspot', sa.Boolean(), nullable=True),
                    sa.Column('domain_name', sa.String(), nullable=True),
                    sa.Column('service_provider_roaming_enabled', sa.Boolean(), nullable=True),
                    sa.Column('roaming_consortium_ois', sa.String(), nullable=True),
                    sa.Column('nai_realm_names', sa.String(), nullable=True),
                    sa.Column('mccs_and_mncs', sa.String(), nullable=True),
                    sa.Column('displayed_operator_name', sa.String(), nullable=True),
                    sa.Column('captive_bypass', sa.Boolean(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('tls_certificate_required', sa.Boolean(), nullable=True),
                    sa.Column('payload_certificate_uuid', commandment.dbtypes.GUID(), nullable=True),
                    sa.Column('proxy_type', sa.String(), nullable=True),
                    sa.Column('proxy_server', sa.String(), nullable=True),
                    sa.Column('proxy_server_port', sa.Integer(), nullable=True),
                    sa.Column('proxy_username', sa.String(), nullable=True),
                    sa.Column('proxy_password', sa.String(), nullable=True),
                    sa.Column('proxy_pac_url', sa.String(), nullable=True),
                    sa.Column('proxy_pac_fallback_allowed', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('wifi_payload')
