import datetime
from abc import ABC, abstractmethod
import ulid
from sqlalchemy.exc import IntegrityError

from src.database import User, EmailVerificationCode
from src.pydantic_models import RegistrationForm, AuthorizationForm
from src.repositories import UserRepositoryProtocol, EmailVerificationCodeRepositoryProtocol
from src.services import EmailVerificationServiceProtocol
from src.utils import PasswordHasherProtocol


class UserAlreadyExists(Exception):
    pass

class UserAuthServiceProtocol(ABC):
    @abstractmethod
    async def register_user(self, data: RegistrationForm) -> tuple[User,str]: ...
    @abstractmethod
    async def authorize_user(self, data: AuthorizationForm) -> User: ...


class UserAuthService(UserAuthServiceProtocol):
    def __init__(self, user_repo: UserRepositoryProtocol, code_repo: EmailVerificationCodeRepositoryProtocol, email_service: EmailVerificationServiceProtocol, password_hasher: PasswordHasherProtocol):
        self.user_repo = user_repo
        self.code_repo = code_repo
        self.email_service = email_service
        self.password_hasher = password_hasher

    async def register_user(self, data: RegistrationForm) -> tuple[User,str]:
        if await self.user_repo.get_user_by_email(str(data.email)):
            raise UserAlreadyExists("Email already registered")
        if await self.user_repo.get_user_by_username(data.username):
            raise UserAlreadyExists("Username already registered")

        hashed_password = await self.password_hasher.hash_password(data.password)

        current_datetime = datetime.datetime.now(datetime.timezone.utc)
        user = User(id=ulid.ulid(),
                    username=data.username,
                    email=data.email,
                    hashed_password=hashed_password,
                    verified=0,
                    created_at=current_datetime)
        try:
            saved = await self.user_repo.save(user)
        except IntegrityError:
            raise UserAlreadyExists("User with this username/email already exists")

        verification_code = self.email_service.generate_verification_code()
        hashed_code = await self.password_hasher.hash_password(verification_code)
        code_obj = EmailVerificationCode(
            user_id=saved.id,
            hashed_code=hashed_code,
            expires_at=current_datetime + datetime.timedelta(minutes=15),
            tries_left=3
        )

        await self.code_repo.save(code_obj)

        return saved, verification_code

    async def authorize_user(self, data: AuthorizationForm) -> User:
        pass