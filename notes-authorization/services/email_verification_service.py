from abc import ABC, abstractmethod


class EmailVerificationServiceProtocol(ABC):
    @abstractmethod
    async def generate_verification_code(self, email:str) -> str: ...

    @abstractmethod
    async def send_verification_email(self, email:str, code:str) -> None: ...