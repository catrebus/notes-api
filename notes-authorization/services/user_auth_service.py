from abc import ABC, abstractmethod

from database import User
from pydantic_models import RegistrationForm, AuthorizationForm


class UserAlreadyExists(Exception):
    pass

class UserAuthServiceProtocol(ABC):
    @abstractmethod
    async def register_user(self, data: RegistrationForm) -> User: ...
    @abstractmethod
    async def authorize_user(self, data: AuthorizationForm) -> User: ...


class UserAuthService(UserAuthServiceProtocol):
    pass