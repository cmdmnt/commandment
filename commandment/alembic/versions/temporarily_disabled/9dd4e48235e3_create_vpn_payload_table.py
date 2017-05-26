"""Create vpn_payload table

Revision ID: 9dd4e48235e3
Revises: e5840df9a88a
Create Date: 2017-05-19 19:59:55.582629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dd4e48235e3'
down_revision = 'e5840df9a88a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('vpn_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_defined_name', sa.String(), nullable=True),
                    sa.Column('override_primary', sa.Boolean(), nullable=True),
                    sa.Column('vpn_type', sa.Enum('L2TP', 'PPTP', 'IPSec', 'IKEv2', 'AlwaysOn', 'VPN', name='vpntype'), nullable=False),
                    sa.Column('vpn_sub_type', sa.String(), nullable=True),
                    sa.Column('provider_bundle_identifier', sa.String(), nullable=True),
                    sa.Column('on_demand_enabled', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('vpn_payload')
