"""Create device_users table

Revision ID: 0c4c448f4daf
Revises: 7d578eb75092
Create Date: 2017-05-18 22:32:52.087025

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


# revision identifiers, used by Alembic.
revision = '0c4c448f4daf'
down_revision = '7d578eb75092'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('device_users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('udid', commandment.dbtypes.GUID(), nullable=False),
                    sa.Column('user_id', commandment.dbtypes.GUID(), nullable=False),
                    sa.Column('long_name', sa.String(), nullable=True),
                    sa.Column('short_name', sa.String(), nullable=True),
                    sa.Column('need_sync_response', sa.Boolean(), nullable=True),
                    sa.Column('user_configuration', sa.Boolean(), nullable=True),
                    sa.Column('digest_challenge', sa.String(), nullable=True),
                    sa.Column('auth_token', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('device_users')
