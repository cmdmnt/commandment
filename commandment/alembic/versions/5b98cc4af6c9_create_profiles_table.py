"""Create profiles table

Revision ID: 5b98cc4af6c9
Revises: e78274be170e
Create Date: 2017-05-19 19:30:47.058720

"""
from alembic import op
import sqlalchemy as sa
import commandment.dbtypes

# revision identifiers, used by Alembic.
revision = '5b98cc4af6c9'
down_revision = 'e78274be170e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('profiles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('data', sa.LargeBinary(), nullable=True),
                    sa.Column('payload_type', sa.String(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('display_name', sa.String(), nullable=True),
                    sa.Column('expiration_date', sa.DateTime(), nullable=True),
                    sa.Column('identifier', sa.String(), nullable=False),
                    sa.Column('organization', sa.String(), nullable=True),
                    sa.Column('uuid', commandment.dbtypes.GUID(), nullable=True),
                    sa.Column('removal_disallowed', sa.Boolean(), nullable=True),
                    sa.Column('version', sa.Integer(), nullable=True),
                    sa.Column('scope', sa.Enum('User', 'System', name='payloadscope'), nullable=True),
                    sa.Column('removal_date', sa.DateTime(), nullable=True),
                    sa.Column('duration_until_removal', sa.BigInteger(), nullable=True),
                    sa.Column('consent_en', sa.Text(), nullable=True),
                    sa.Column('is_encrypted', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_profiles_uuid'), 'profiles', ['uuid'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_profiles_uuid'), table_name='profiles')
    op.drop_table('profiles')
