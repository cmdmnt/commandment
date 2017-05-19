"""Create device_group_devices table

Revision ID: ba4849d8c8ad
Revises: a1d5ffaa2092
Create Date: 2017-05-19 19:44:37.403554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba4849d8c8ad'
down_revision = 'a1d5ffaa2092'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('device_group_devices',
                    sa.Column('device_group_id', sa.Integer(), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['device_group_id'], ['device_groups.id'], ),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.PrimaryKeyConstraint('device_group_id', 'device_id')
                    )


def downgrade():
    op.drop_table('device_group_devices')
