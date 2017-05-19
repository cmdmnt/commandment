"""Create energy_saver_payload table

Revision ID: 18412434fb57
Revises: 323a90039a6a
Create Date: 2017-05-19 19:53:03.142964

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = '18412434fb57'
down_revision = '323a90039a6a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('energy_saver_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('destroy_fv_key_on_standby', sa.Boolean(), nullable=True),
                    sa.Column('sleep_disabled', sa.Boolean(), nullable=True),
                    sa.Column('desktop_acpower_profilenumber', sa.Integer(), nullable=True),
                    sa.Column('portable_acpower_profilenumber', sa.Integer(), nullable=True),
                    sa.Column('portable_battery_profilenumber', sa.Integer(), nullable=True),
                    sa.Column('desktop_acpower', commandment.dbtypes.JSONEncodedDict(), nullable=True),
                    sa.Column('portable_acpower', commandment.dbtypes.JSONEncodedDict(), nullable=True),
                    sa.Column('portable_battery', commandment.dbtypes.JSONEncodedDict(), nullable=True),
                    sa.Column('desktop_schedule', commandment.dbtypes.JSONEncodedDict(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('energy_saver_payload')
