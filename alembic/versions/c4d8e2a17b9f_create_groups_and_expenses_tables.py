"""create_groups_and_expenses_tables

Revision ID: c4d8e2a17b9f
Revises: ffbfb6dd751d
Create Date: 2026-06-06 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4d8e2a17b9f'
down_revision: Union[str, Sequence[str], None] = 'ffbfb6dd751d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('groups',
    sa.Column('group_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_table('group_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group_id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expenses',
    sa.Column('expense_id', sa.String(length=36), nullable=False),
    sa.Column('group_id', sa.String(length=36), nullable=False),
    sa.Column('paid_by', sa.String(length=36), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['paid_by'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('expense_id')
    )
    op.create_table('expense_shares',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('expense_id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('share_amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['expense_id'], ['expenses.expense_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('expense_shares')
    op.drop_table('expenses')
    op.drop_table('group_members')
    op.drop_table('groups')
