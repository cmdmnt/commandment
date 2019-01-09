"""create_managed_applications_table

Revision ID: fa4d91c6aacf
Revises: 3dbf6db7f9eb
Create Date: 2019-01-10 10:01:10.750225

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'fa4d91c6aacf'
down_revision = '3dbf6db7f9eb'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()


def downgrade():
    schema_downgrades()


def schema_upgrades():
    op.create_table('managed_applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('bundle_id', sa.String(), nullable=True),
        sa.Column('external_version_id', sa.Integer(), nullable=True),
        sa.Column('has_configuration', sa.Boolean(), nullable=True),
        sa.Column('has_feedback', sa.Boolean(), nullable=True),
        sa.Column('is_validated', sa.Boolean(), nullable=True),
        sa.Column('management_flags', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('application_id', sa.Integer(), nullable=True),
        sa.Column('ia_command_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.ForeignKeyConstraint(['ia_command_id'], ['commands.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def schema_downgrades():
    op.drop_table('managed_applications')
