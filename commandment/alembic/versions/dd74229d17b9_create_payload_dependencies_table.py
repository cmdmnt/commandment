"""Create payload_dependencies table

Revision ID: dd74229d17b9
Revises: d65049bf4b91
Create Date: 2017-05-19 20:02:17.116286

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = 'dd74229d17b9'
down_revision = 'd65049bf4b91'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('payload_dependencies',
                    sa.Column('payload_uuid', commandment.dbtypes.GUID(), nullable=True),
                    sa.Column('depends_on_payload_uuid', commandment.dbtypes.GUID(), nullable=True),
                    sa.ForeignKeyConstraint(['depends_on_payload_uuid'], ['payloads.uuid'], ),
                    sa.ForeignKeyConstraint(['payload_uuid'], ['payloads.uuid'], )
                    )


def downgrade():
    op.drop_table('payload_dependencies')
