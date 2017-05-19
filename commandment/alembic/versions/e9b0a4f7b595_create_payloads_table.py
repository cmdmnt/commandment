"""Create payloads table

Revision ID: e9b0a4f7b595
Revises: 0c4c448f4daf
Create Date: 2017-05-18 22:34:37.838655

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = 'e9b0a4f7b595'
down_revision = '0c4c448f4daf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('payloads',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.Column('version', sa.Integer(), nullable=True),
                    sa.Column('identifier', sa.String(), nullable=True),
                    sa.Column('uuid', commandment.dbtypes.GUID(), nullable=False),
                    sa.Column('display_name', sa.String(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('organization', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_payloads_type'), 'payloads', ['type'], unique=False)
    op.create_index(op.f('ix_payloads_uuid'), 'payloads', ['uuid'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_payloads_uuid'), table_name='payloads')
    op.drop_index(op.f('ix_payloads_type'), table_name='payloads')
    op.drop_table('payloads')
