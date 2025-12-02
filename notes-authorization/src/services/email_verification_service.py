import logging
import secrets
from abc import ABC, abstractmethod
from email.message import EmailMessage

import aiosmtplib


class EmailVerificationServiceProtocol(ABC):
    @abstractmethod
    def generate_verification_code(self) -> str: ...

    @abstractmethod
    async def send_verification_email(self, email:str, code:str) -> None: ...


class EmailVerificationService(EmailVerificationServiceProtocol):
    def __init__(self, smtp_user: str, smtp_password: str, smtp_hostname:str):
        self._smtp_user = smtp_user
        self._smtp_password = smtp_password
        self._smtp_hostname = smtp_hostname

    def generate_verification_code(self) -> str:
        return f"{secrets.randbelow(1_000_000):06d}"

    async def send_verification_email(self, email: str, code: str) -> None:
        message = EmailMessage()
        message['From'] = self._smtp_user
        message['To'] = email
        message['Subject'] = 'Verify your email'
        message.set_content(f'Your verification code: {code}')
        try:
            await aiosmtplib.send(
                message,
                hostname=self._smtp_hostname,
                port=465,
                username=self._smtp_user,
                password=self._smtp_password,
                use_tls=True
            )
        except Exception as e:
            logging.warning(e)