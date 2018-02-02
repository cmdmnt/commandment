"""Create commands table

Revision ID: 71ecf957301a
Revises: af4ba256efde
Create Date: 2017-05-19 19:38:21.450906

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = '71ecf957301a'
down_revision = 'af4ba256efde'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('commands',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('request_type', sa.String(), nullable=False),
                    sa.Column('uuid', commandment.dbtypes.GUID(), nullable=False),
                    sa.Column('parameters', commandment.dbtypes.JSONEncodedDict(), nullable=True),
                    sa.Column('status', sa.String(length=40), nullable=False),
                    sa.Column('queued_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
                    sa.Column('sent_at', sa.DateTime(), nullable=True),
                    sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
                    sa.Column('after', sa.DateTime(), nullable=True),
                    sa.Column('ttl', sa.Integer(), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_commands_status'), 'commands', ['status'], unique=False)
    op.create_index(op.f('ix_commands_uuid'), 'commands', ['uuid'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_commands_uuid'), table_name='commands')
    op.drop_index(op.f('ix_commands_status'), table_name='commands')
    op.drop_table('commands')
