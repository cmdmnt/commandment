"""Create mdm_payload table

Revision ID: 4eddbcb30464
Revises: 18412434fb57
Create Date: 2017-05-19 19:54:24.264198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eddbcb30464'
down_revision = '18412434fb57'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mdm_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('identity_certificate_uuid', commandment.dbtypes.GUID(), nullable=False),
                    sa.Column('topic', sa.String(), nullable=False),
                    sa.Column('server_url', sa.String(), nullable=False),
                    sa.Column('server_capabilities', sa.String(), nullable=True),
                    sa.Column('sign_message', sa.Boolean(), nullable=True),
                    sa.Column('check_in_url', sa.String(), nullable=True),
                    sa.Column('check_out_when_removed', sa.Boolean(), nullable=True),
                    sa.Column('access_rights', sa.Integer(), nullable=True),
                    sa.Column('use_development_apns', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('mdm_payload')
