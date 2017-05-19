"""Create organizations table

Revision ID: e78274be170e
Revises: e9b0a4f7b595
Create Date: 2017-05-19 19:28:42.596244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e78274be170e'
down_revision = 'e9b0a4f7b595'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('organizations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('payload_prefix', sa.String(), nullable=True),
                    sa.Column('x509_ou', sa.String(length=32), nullable=True),
                    sa.Column('x509_o', sa.String(length=64), nullable=True),
                    sa.Column('x509_st', sa.String(length=128), nullable=True),
                    sa.Column('x509_c', sa.String(length=2), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('organizations')
