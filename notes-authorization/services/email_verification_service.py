import secrets
from abc import ABC, abstractmethod


class EmailVerificationServiceProtocol(ABC):
    @abstractmethod
    async def generate_verification_code(self) -> str: ...

    @abstractmethod
    async def send_verification_email(self, email:str, code:str) -> None: ...


class EmailVerificationService(EmailVerificationServiceProtocol):

    async def generate_verification_code(self) -> str:
        return f"{secrets.randbelow(1_000_000):06d}"

    async def send_verification_email(self, email: str, code: str) -> None:
        print('sending verification code to email')