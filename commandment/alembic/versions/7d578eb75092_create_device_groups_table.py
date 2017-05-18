"""Create device_groups table

Revision ID: 7d578eb75092
Revises: 71818e983100
Create Date: 2017-05-18 22:31:16.686848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d578eb75092'
down_revision = '71818e983100'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('device_groups',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('device_groups')
