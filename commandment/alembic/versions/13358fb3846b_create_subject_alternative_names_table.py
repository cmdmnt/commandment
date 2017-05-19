"""Create subject_alternative_names table

Revision ID: 13358fb3846b
Revises: ea34ae3f1e7e
Create Date: 2017-05-19 19:48:09.977131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13358fb3846b'
down_revision = 'ea34ae3f1e7e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('subject_alternative_names',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('discriminator', sa.Enum('RFC822Name', 'DNSName', 'UniformResourceIdentifier', 'DirectoryName', 'RegisteredID', 'IPAddress', 'OtherName', name='subjectalternativenametype'), nullable=False),
                    sa.Column('str_value', sa.String(), nullable=True),
                    sa.Column('octet_value', sa.LargeBinary(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('subject_alternative_names')
