import asyncio
from abc import ABC, abstractmethod

import bcrypt


class PasswordHasherProtocol(ABC):

    @abstractmethod
    async def hash_password(self, password: str) -> str: ...

    @abstractmethod
    async def verify_password(self, password: str, hashed_password: str) -> bool: ...


class PasswordHasher(PasswordHasherProtocol):

    async def hash_password(self, password: str) -> str:
        return await asyncio.to_thread(bcrypt.hashpw, password.encode(), bcrypt.gensalt())

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return asyncio.to_thread(bcrypt.checkpw, password.encode(), hashed_password.encode())