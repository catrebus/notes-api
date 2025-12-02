from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import EmailVerificationCodeRepositoryProtocol
from src.database.db_models import EmailVerificationCode


class EmailVerificationCodeRepository(EmailVerificationCodeRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, code: EmailVerificationCode) -> Optional[EmailVerificationCode]:
        """Сохранение кода в бд"""
        self.session.add(code)
        await self.session.commit()

        await self.session.refresh(code)
        return code

    async def get_code_by_user_id(self, user_id: str) -> Optional[EmailVerificationCode]:
        res = await self.session.execute(select(EmailVerificationCode).where(EmailVerificationCode.user_id == user_id))
        return res.scalar_one_or_none()

    async def decrement_tries(self, code_obj: EmailVerificationCode) -> None:
        if code_obj.tries_left <= 0:
            return
        code_obj.tries_left -= 1
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        await self.session.refresh(code_obj)

    async def delete_code(self, code_obj: EmailVerificationCode) -> None:
        await self.session.delete(code_obj)
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
        raise
