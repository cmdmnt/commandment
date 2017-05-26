"""Create email_payload table

Revision ID: 323a90039a6a
Revises: e47e29a9537c
Create Date: 2017-05-19 19:52:05.726744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '323a90039a6a'
down_revision = 'e47e29a9537c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('email_payload',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email_account_description', sa.String(), nullable=True),
                    sa.Column('email_account_name', sa.String(), nullable=True),
                    sa.Column('email_account_type', sa.Enum('POP', 'IMAP', name='emailaccounttype'), nullable=False),
                    sa.Column('email_address', sa.String(), nullable=True),
                    sa.Column('incoming_auth', sa.Enum('Password', 'CRAM_MD5', 'NTLM', 'HTTP_MD5', 'ENone', name='emailauthenticationtype'), nullable=False),
                    sa.Column('incoming_host', sa.String(), nullable=False),
                    sa.Column('incoming_port', sa.Integer(), nullable=True),
                    sa.Column('incoming_use_ssl', sa.Boolean(), nullable=True),
                    sa.Column('incoming_username', sa.String(), nullable=False),
                    sa.Column('incoming_password', sa.String(), nullable=True),
                    sa.Column('outgoing_password', sa.String(), nullable=True),
                    sa.Column('outgoing_incoming_same', sa.Boolean(), nullable=True),
                    sa.Column('outgoing_auth', sa.Enum('Password', 'CRAM_MD5', 'NTLM', 'HTTP_MD5', 'ENone', name='emailauthenticationtype'), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['payloads.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('email_payload')
