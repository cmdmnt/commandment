"""Create OAuth Server Models

Revision ID: 80fa1767c7e2
Revises: fa4d91c6aacf
Create Date: 2019-05-20 20:47:04.928849

"""

# From: http://alembic.zzzcomputing.com/en/latest/cookbook.html#conditional-migration-elements

from alembic import op
import sqlalchemy as sa
import commandment.dbtypes


from alembic import context

# revision identifiers, used by Alembic.
revision = '80fa1767c7e2'
down_revision = 'fa4d91c6aacf'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()


def downgrade():
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    op.create_table('oauth2_clients',
    sa.Column('client_id', sa.String(length=48), nullable=True),
    sa.Column('client_secret', sa.String(length=120), nullable=True),
    sa.Column('issued_at', sa.Integer(), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=False),
    sa.Column('redirect_uri', sa.Text(), nullable=True),
    sa.Column('token_endpoint_auth_method', sa.String(length=48), nullable=True),
    sa.Column('grant_type', sa.Text(), nullable=False),
    sa.Column('response_type', sa.Text(), nullable=False),
    sa.Column('scope', sa.Text(), nullable=False),
    sa.Column('client_name', sa.String(length=100), nullable=True),
    sa.Column('client_uri', sa.Text(), nullable=True),
    sa.Column('logo_uri', sa.Text(), nullable=True),
    sa.Column('contact', sa.Text(), nullable=True),
    sa.Column('tos_uri', sa.Text(), nullable=True),
    sa.Column('policy_uri', sa.Text(), nullable=True),
    sa.Column('jwks_uri', sa.Text(), nullable=True),
    sa.Column('jwks_text', sa.Text(), nullable=True),
    sa.Column('i18n_metadata', sa.Text(), nullable=True),
    sa.Column('software_id', sa.String(length=36), nullable=True),
    sa.Column('software_version', sa.String(length=48), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('oauth2_clients', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_oauth2_clients_client_id'), ['client_id'], unique=False)

    op.create_table('oauth2_tokens',
    sa.Column('client_id', sa.String(length=48), nullable=True),
    sa.Column('token_type', sa.String(length=40), nullable=True),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('scope', sa.Text(), nullable=True),
    sa.Column('revoked', sa.Boolean(), nullable=True),
    sa.Column('issued_at', sa.Integer(), nullable=False),
    sa.Column('expires_in', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token')
    )
    with op.batch_alter_table('oauth2_tokens', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_oauth2_tokens_refresh_token'), ['refresh_token'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def schema_downgrades():
    op.drop_table('users')
    with op.batch_alter_table('oauth2_tokens', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_oauth2_tokens_refresh_token'))

    op.drop_table('oauth2_tokens')
    with op.batch_alter_table('oauth2_clients', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_oauth2_clients_client_id'))

    op.drop_table('oauth2_clients')
