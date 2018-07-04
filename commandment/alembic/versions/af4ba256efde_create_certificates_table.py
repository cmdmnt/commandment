"""Create certificates table

Revision ID: af4ba256efde
Revises: 0ab46b2f6d8c
Create Date: 2017-05-19 19:36:12.171390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af4ba256efde'
down_revision = '0ab46b2f6d8c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('certificates',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('pem_data', sa.Text(), nullable=False),
                    sa.Column('rsa_private_key_id', sa.Integer(), nullable=True),
                    sa.Column('x509_cn', sa.String(length=64), nullable=True),
                    sa.Column('x509_ou', sa.String(length=32), nullable=True),
                    sa.Column('x509_o', sa.String(length=64), nullable=True),
                    sa.Column('x509_c', sa.String(length=2), nullable=True),
                    sa.Column('x509_st', sa.String(length=128), nullable=True),
                    sa.Column('not_before', sa.DateTime(), nullable=False),
                    sa.Column('not_after', sa.DateTime(), nullable=False),
                    sa.Column('serial', sa.BigInteger(), nullable=True),
                    sa.Column('fingerprint', sa.String(length=64), nullable=False),
                    sa.Column('push_topic', sa.String(), nullable=True),
                    sa.Column('discriminator', sa.String(length=20), nullable=True),
                    sa.ForeignKeyConstraint(['rsa_private_key_id'], ['rsa_private_keys.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_certificates_fingerprint'), 'certificates', ['fingerprint'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_certificates_fingerprint'), table_name='certificates')
    op.drop_table('certificates')
