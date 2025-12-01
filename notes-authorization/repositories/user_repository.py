from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from repositories import UserRepositoryProtocol


class UserRepository(UserRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> Optional[User]:
        """Добавление нового пользователя в бд"""
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        await self.session.refresh(user)
        return user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по username"""
        res = await self.session.execute(select(User).where(User.username == username))
        return res.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        res = await self.session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Получение пользователя по id"""
        res = await self.session.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()

    async def is_verified(self, username: str) -> bool:
        res = await self.session.execute(select(User.verified).where(User.username == username))
        return bool(res.scalar())

    async def set_verified(self, username: str, verified: bool) -> None:
        user = await self.session.execute(select(User).where(User.username == username))
        user.verified = verified
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
