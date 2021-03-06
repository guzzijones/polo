"""change book column

Revision ID: 736a30c7528a
Revises: e767fae8d3af
Create Date: 2018-05-07 06:24:25.968404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '736a30c7528a'
down_revision = 'e767fae8d3af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade', sa.Column('book', sa.String(length=10), nullable=False))
    op.drop_column('trade', 'cur_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade', sa.Column('cur_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('trade', 'book')
    # ### end Alembic commands ###
