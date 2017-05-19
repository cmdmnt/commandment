"""Create profile_payloads table

Revision ID: ea34ae3f1e7e
Revises: ba4849d8c8ad
Create Date: 2017-05-19 19:45:34.375475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea34ae3f1e7e'
down_revision = 'ba4849d8c8ad'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('profile_payloads',
                    sa.Column('profile_id', sa.Integer(), nullable=True),
                    sa.Column('payload_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['payload_id'], ['payloads.id'], ),
                    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], )
                    )


def downgrade():
    op.drop_table('profile_payloads')
