from fastapi.params import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.authorization_config import Config
from src.repositories import UserRepository, EmailVerificationCodeRepository
from src.services.email_verification_service import EmailVerificationService
from src.services.user_auth_service import UserAuthService
from src.utils import PasswordHasher


class Container:
    def __init__(self):
        # ------ Config ------
        self.config = Config()

        # ------ Database ------
        self.engine = create_async_engine(self.config.AUTHORIZATION_DATABASE_URL, echo=True)
        self.SessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)

        # ------ Services that are singletons ------
        self.email_verification_service = EmailVerificationService(smtp_user=self.config.AUTHORIZATION_SMTP_USER,
                                                                   smtp_hostname=self.config.AUTHORIZATION_SMTP_HOSTNAME,
                                                                   smtp_password=self.config.AUTHORIZATION_SMTP_PASSWORD)
        self.password_hasher = PasswordHasher()

    # ------ Dependencies ------
    async def get_session(self) -> AsyncSession:
        async with self.SessionLocal() as session:
            yield session

    def get_user_repository(self,
                                  session: AsyncSession = Depends(get_session)
                                  ) -> UserRepository:
        return UserRepository(session=session)

    def get_email_verification_code_repository(self,
                                                     session: AsyncSession = Depends(get_session)
                                                     ) -> EmailVerificationCodeRepository:
        return EmailVerificationCodeRepository(session=session)

    def get_user_auth_service(self,
                                    user_repository: UserRepository = Depends(get_user_repository),
                                    email_verification_code_repository: EmailVerificationCodeRepository = Depends(get_email_verification_code_repository),
                                    ) -> UserAuthService:
        return UserAuthService(user_repo=user_repository,
                               code_repo=email_verification_code_repository,
                               email_service=self.email_verification_service,
                               password_hasher=self.password_hasher)


container = Container()