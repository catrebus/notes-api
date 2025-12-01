import datetime

from sqlalchemy import DateTime, Index, String, ForeignKeyConstraint, Integer, text
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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

    email_verification_code: Mapped[list['EmailVerificationCode']] = relationship('EmailVerificationCode', back_populates='user')


class EmailVerificationCode(Base):
    __tablename__ = 'email_verification_code'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id'], name='user_id_email_verification_code'),
        Index('user_id_email_verification_code_idx', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_code: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    tries_left: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'3'"))

    user: Mapped['User'] = relationship('User', back_populates='email_verification_code')

