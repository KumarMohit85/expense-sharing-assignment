from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    user_id:Mapped[str]=mapped_column(
        String(36),
        primary_key= True,
        default = lambda:str(uuid4())
        )
    
    name:Mapped[str] = mapped_column(
        String(100),
        nullable=False
        )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )