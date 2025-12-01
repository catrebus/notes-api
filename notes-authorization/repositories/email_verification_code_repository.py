from sqlalchemy.ext.asyncio import AsyncSession

from repositories import EmailVerificationCodeRepositoryProtocol


class EmailVerificationCodeRepository(EmailVerificationCodeRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session