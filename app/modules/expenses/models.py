from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    expense_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    group_id: Mapped[str] = mapped_column(
        ForeignKey("groups.group_id"),
        nullable=False
    )

    paid_by: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )


class ExpenseShare(Base):
    __tablename__ = "expense_shares"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    expense_id: Mapped[str] = mapped_column(
        ForeignKey("expenses.expense_id"),
        nullable=False
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    share_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
