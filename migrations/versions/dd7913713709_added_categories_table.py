"""Added categories table

Revision ID: dd7913713709
Revises: 114e6b9ab465
Create Date: 2020-02-11 22:42:54.358243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd7913713709'
down_revision = '114e6b9ab465'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('parent_category_id', sa.Integer(), nullable=True),
    sa.Column('category_name', sa.String(length=40), nullable=True),
    sa.Column('user_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['parent_category_id'], ['category.category_id'], name=op.f('fk_category_parent_category_id_category')),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name=op.f('fk_category_user_id_user')),
    sa.PrimaryKeyConstraint('category_id', name=op.f('pk_category'))
    )
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_transaction_category_id_category'), 'category', ['category_id'], ['category_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_transaction_category_id_category'), type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('category')
    # ### end Alembic commands ###
