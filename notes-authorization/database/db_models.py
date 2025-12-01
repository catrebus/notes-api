import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('email_UNIQUE', 'email', unique=True),
        Index('login_UNIQUE', 'username', unique=True)
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    verified: Mapped[int] = mapped_column(TINYINT, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
