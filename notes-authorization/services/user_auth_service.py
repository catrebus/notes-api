import datetime
from abc import ABC, abstractmethod
from zoneinfo import ZoneInfo
import ulid
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

from database import User
from pydantic_models import RegistrationForm, AuthorizationForm
from repositories import UserRepositoryProtocol
from services import EmailVerificationServiceProtocol


class UserAlreadyExists(Exception):
    pass

class UserAuthServiceProtocol(ABC):
    @abstractmethod
    async def register_user(self, data: RegistrationForm) -> tuple[User,str]: ...
    @abstractmethod
    async def authorize_user(self, data: AuthorizationForm) -> User: ...


class UserAuthService(UserAuthServiceProtocol):
    def __init__(self, user_repo: UserRepositoryProtocol, email_service: EmailVerificationServiceProtocol):
        self.user_repo = user_repo
        self.email_service = email_service

    async def register_user(self, data: RegistrationForm) -> tuple[User,str]:
        if await self.user_repo.get_user_by_email(str(data.email)):
            raise UserAlreadyExists("Email already registered")
        if await self.user_repo.get_user_by_username(data.username):
            raise UserAlreadyExists("Username already registered")

        hashed_password = bcrypt.hash(data.password)

        user = User(id=ulid.ulid(),
                    username=data.username,
                    email=data.email,
                    hashed_password=hashed_password,
                    verified=0,
                    created_at=datetime.datetime.now(ZoneInfo("Europe/Moscow")))
        try:
            saved = await self.user_repo.save(user)
        except IntegrityError:
            raise UserAlreadyExists("User with this username/email already exists")

        verification_code = await self.email_service.generate_verification_code()

        return saved, verification_code

    async def authorize_user(self, data: AuthorizationForm) -> User:
        pass