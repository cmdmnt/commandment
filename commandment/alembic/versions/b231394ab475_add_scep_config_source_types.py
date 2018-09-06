"""add scep_config source types

Revision ID: b231394ab475
Revises: a3ddaad5c358
Create Date: 2018-09-07 07:50:10.467330

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = 'b231394ab475'
down_revision = 'a3ddaad5c358'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()


def downgrade():
    schema_downgrades()


def schema_upgrades():
    op.add_column('scep_config', sa.Column('source_type', sa.Enum('InternalPKCS12', 'InternalSCEP', 'ExternalSCEP', name='deviceidentitysources'), nullable=True))


def schema_downgrades():
    op.drop_column('scep_config', 'source_type')

