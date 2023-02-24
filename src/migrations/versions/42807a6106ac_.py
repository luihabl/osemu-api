"""empty message

Revision ID: 42807a6106ac
Revises: 
Create Date: 2023-02-23 14:27:29.919900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42807a6106ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
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
    op.create_table('license',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('programming_language',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('console',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
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
    op.drop_table('console')
    op.drop_table('programming_language')
    op.drop_table('license')
    op.drop_table('emulator')
    op.drop_table('company')
    # ### end Alembic commands ###
