"""create_tags

Revision ID: 70ff84113e8f
Revises: 7ae48ae412d7
Create Date: 2017-06-20 17:13:11.572353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70ff84113e8f'
down_revision = 'dd74229d17b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tags',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('color', sa.String(length=6), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('profile_tags',
                    sa.Column('profile_id', sa.Integer(), nullable=True),
                    sa.Column('tag_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
                    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
                    )
    op.create_table('device_tags',
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('tag_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
                    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
                    )


def downgrade():
    op.drop_table('device_tags')
    op.drop_table('profile_tags')
    op.drop_table('tags')
