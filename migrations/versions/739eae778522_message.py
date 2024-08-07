"""message

Revision ID: 739eae778522
Revises: 982f057efce9
Create Date: 2024-06-29 22:38:09.753034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '739eae778522'
down_revision = '982f057efce9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('restaurant_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('pizza_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_restaurant_id_restaurants'), 'restaurants', ['restaurant_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_restaurant_pizzas_pizza_id_pizzas'), 'pizzas', ['pizza_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant_pizzas', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_pizza_id_pizzas'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_restaurant_pizzas_restaurant_id_restaurants'), type_='foreignkey')
        batch_op.drop_column('pizza_id')
        batch_op.drop_column('restaurant_id')

    # ### end Alembic commands ###
