"""add large trade table

Revision ID: fffc6ee85cec
Revises: 179c26e15342
Create Date: 2018-05-08 07:35:40.727091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fffc6ee85cec'
down_revision = '179c26e15342'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('large_trade',
    sa.Column('trade', sa.String(length=1), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('threshold', sa.Integer(), nullable=False),
    sa.Column('book', sa.String(length=10), nullable=False),
    sa.Column('type', sa.String(length=5), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'threshold', 'book')
    )
    op.drop_column('trade', 'large')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade', sa.Column('large', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_table('large_trade')
    # ### end Alembic commands ###
