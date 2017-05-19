"""Create rsa_private_keys table

Revision ID: e58afdc17baa
Revises: 5b98cc4af6c9
Create Date: 2017-05-19 19:32:28.454940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e58afdc17baa'
down_revision = '5b98cc4af6c9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('rsa_private_keys',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('pem_data', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('rsa_private_keys')
