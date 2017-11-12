"""Create users table

Revision ID: 0ab46b2f6d8c
Revises: f5237c7e2374
Create Date: 2017-05-19 19:35:12.126022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ab46b2f6d8c'
down_revision = 'f5237c7e2374'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('fullname', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
