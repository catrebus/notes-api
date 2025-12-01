from typing import Protocol

from starlette.requests import Request


class AuthServiceProtocol(Protocol):
    async def is_authorized(self, request: Request) -> bool: ...