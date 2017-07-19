"""empty message

Revision ID: 8c866896f76e
Revises: 0e5babc5b9ee
Create Date: 2017-07-19 12:57:58.086196

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '8c866896f76e'
down_revision = '0e5babc5b9ee'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    op.create_table('dep_profile_anchor_certificates',
    sa.Column('dep_profile_id', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ),
    sa.ForeignKeyConstraint(['dep_profile_id'], ['dep_profiles.id'], )
    )
    op.create_table('dep_profile_supervision_certificates',
    sa.Column('dep_profile_id', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ),
    sa.ForeignKeyConstraint(['dep_profile_id'], ['dep_profiles.id'], )
    )


def schema_downgrades():
    """schema downgrade migrations go here."""
    op.drop_table('dep_profile_supervision_certificates')
    op.drop_table('dep_profile_anchor_certificates')


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
