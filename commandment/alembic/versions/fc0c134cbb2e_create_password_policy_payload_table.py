"""Create password_policy_payload table

Revision ID: fc0c134cbb2e
Revises: 4eddbcb30464
Create Date: 2017-05-19 19:56:45.009648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc0c134cbb2e'
down_revision = '4eddbcb30464'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('password_policy_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('allow_simple', sa.Boolean(), nullable=True),
                    sa.Column('force_pin', sa.Boolean(), nullable=True),
                    sa.Column('max_failed_attempts', sa.Integer(), nullable=True),
                    sa.Column('max_inactivity', sa.Integer(), nullable=True),
                    sa.Column('max_pin_age_in_days', sa.Integer(), nullable=True),
                    sa.Column('min_complex_chars', sa.Integer(), nullable=True),
                    sa.Column('min_length', sa.Integer(), nullable=True),
                    sa.Column('require_alphanumeric', sa.Boolean(), nullable=True),
                    sa.Column('pin_history', sa.Integer(), nullable=True),
                    sa.Column('max_grace_period', sa.Integer(), nullable=True),
                    sa.Column('allow_fingerprint_modification', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('password_policy_payload')
