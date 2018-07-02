"""Create installed_certificates table

Revision ID: e16577adc4fd
Revises: 50188ffaf0cd
Create Date: 2017-05-19 19:40:56.436486

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = 'e16577adc4fd'
down_revision = '50188ffaf0cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('installed_certificates',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('device_udid', sa.String(40), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('x509_cn', sa.String(), nullable=True),
                    sa.Column('is_identity', sa.Boolean(), nullable=True),
                    sa.Column('der_data', sa.LargeBinary(), nullable=False),
                    sa.Column('fingerprint_sha256', sa.String(length=64), nullable=False),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_installed_certificates_device_udid'), 'installed_certificates', ['device_udid'], unique=False)
    op.create_index(op.f('ix_installed_certificates_fingerprint_sha256'), 'installed_certificates', ['fingerprint_sha256'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_installed_certificates_fingerprint_sha256'), table_name='installed_certificates')
    op.drop_index(op.f('ix_installed_certificates_device_udid'), table_name='installed_certificates')
    op.drop_table('installed_certificates')

