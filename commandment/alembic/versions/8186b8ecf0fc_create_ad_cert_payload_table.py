"""Create ad_cert_payload table

Revision ID: 8186b8ecf0fc
Revises: 13358fb3846b
Create Date: 2017-05-19 19:49:07.136996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8186b8ecf0fc'
down_revision = '13358fb3846b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ad_cert_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('certificate_description', sa.String(), nullable=True),
                    sa.Column('allow_all_apps_access', sa.Boolean(), nullable=True),
                    sa.Column('cert_server', sa.String(), nullable=False),
                    sa.Column('cert_template', sa.String(), nullable=False),
                    sa.Column('acquisition_mechanism', sa.Enum('RPC', 'HTTP', name='adcertificateacquisitionmechanism'), nullable=True),
                    sa.Column('certificate_authority', sa.String(), nullable=False),
                    sa.Column('renewal_time_interval', sa.Integer(), nullable=True),
                    sa.Column('identity_description', sa.String(), nullable=True),
                    sa.Column('key_is_extractable', sa.Boolean(), nullable=True),
                    sa.Column('prompt_for_credentials', sa.Boolean(), nullable=True),
                    sa.Column('keysize', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('ad_cert_payload')
