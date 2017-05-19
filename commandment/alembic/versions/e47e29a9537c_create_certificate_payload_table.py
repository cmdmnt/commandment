"""Create certificate_payload table

Revision ID: e47e29a9537c
Revises: 072fba4a2256
Create Date: 2017-05-19 19:51:20.672688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e47e29a9537c'
down_revision = '072fba4a2256'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('certificate_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('certificate_file_name', sa.String(), nullable=True),
                    sa.Column('payload_content', sa.LargeBinary(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('certificate_payload')
