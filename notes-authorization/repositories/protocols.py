from abc import ABC, abstractmethod
from typing import Optional

from database import User


class UserRepositoryProtocol(ABC):

    @abstractmethod
    async def save(self, user: User): ...

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