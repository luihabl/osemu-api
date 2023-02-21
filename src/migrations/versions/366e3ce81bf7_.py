"""empty message

Revision ID: 366e3ce81bf7
Revises: 
Create Date: 2023-02-20 21:24:25.342353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '366e3ce81bf7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('console',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('manufacturer', sa.String(length=255), nullable=False),
    sa.CheckConstraint('char_length(manufacturer) > 2', name='manufacturer_min_length'),
    sa.CheckConstraint('char_length(name) > 2', name='name_min_length'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('emulator',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('git_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('emu_console',
    sa.Column('emulator_id', sa.UUID(), nullable=True),
    sa.Column('console_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['console_id'], ['console.id'], ),
    sa.ForeignKeyConstraint(['emulator_id'], ['emulator.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emu_console')
    op.drop_table('emulator')
    op.drop_table('console')
    # ### end Alembic commands ###
