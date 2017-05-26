"""Create ad_payload table

Revision ID: 072fba4a2256
Revises: 8186b8ecf0fc
Create Date: 2017-05-19 19:50:25.537513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '072fba4a2256'
down_revision = '8186b8ecf0fc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ad_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('host_name', sa.String(), nullable=False),
                    sa.Column('user_name', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('ad_organizational_unit', sa.String(), nullable=False),
                    sa.Column('ad_mount_style', sa.Enum('AFP', 'SMB', name='admountstyle'), nullable=False),
                    sa.Column('ad_default_user_shell', sa.String(), nullable=True),
                    sa.Column('ad_map_uid_attribute', sa.String(), nullable=True),
                    sa.Column('ad_map_gid_attribute', sa.String(), nullable=True),
                    sa.Column('ad_map_ggid_attribute', sa.String(), nullable=True),
                    sa.Column('ad_preferred_dc_server', sa.String(), nullable=True),
                    sa.Column('ad_domain_admin_group_list', sa.String(), nullable=True),
                    sa.Column('ad_namespace', sa.Enum('Domain', 'Forest', name='adnamespace'), nullable=True),
                    sa.Column('ad_packet_sign', sa.Enum('Allow', 'Disable', 'Require', name='adpacketsignpolicy'), nullable=True),
                    sa.Column('ad_packet_encrypt', sa.Enum('Allow', 'Disable', 'Require', 'SSL', name='adpacketencryptpolicy'), nullable=True),
                    sa.Column('ad_restrict_ddns', sa.String(), nullable=True),
                    sa.Column('ad_trust_change_pass_interval', sa.Integer(), nullable=True),
                    sa.Column('ad_create_mobile_account_at_login', sa.Boolean(), nullable=True),
                    sa.Column('ad_warn_user_before_creating_ma', sa.Boolean(), nullable=True),
                    sa.Column('ad_force_home_local', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('ad_payload')
