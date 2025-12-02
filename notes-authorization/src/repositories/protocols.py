from abc import ABC, abstractmethod
from typing import Optional

from database import User, EmailVerificationCode


class UserRepositoryProtocol(ABC):

    @abstractmethod
    async def save(self, user: User) -> Optional[User]: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    async def is_verified(self, user_id: str) -> bool: ...

    @abstractmethod
    async def set_verified(self, user_id: str, verified: bool) -> None: ...


class EmailVerificationCodeRepositoryProtocol(ABC):

    @abstractmethod
    async def save(self, email_verification_code: EmailVerificationCode) -> Optional[EmailVerificationCode]: ...

    @abstractmethod
    async def get_code_by_user_id(self, user_id: str) -> Optional[EmailVerificationCode]: ...

    @abstractmethod
    async def decrement_tries(self, code_obj: EmailVerificationCode) -> None: ...

    @abstractmethod
    async def delete_code(self, code_obj: EmailVerificationCode) -> None: ...