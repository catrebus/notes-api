from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from services.request_auth import AuthServiceProtocol


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_service: AuthServiceProtocol):
        super().__init__(app)
        self._auth_service = auth_service

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not await self._auth_service.is_authorized(request):
            return Response('Unauthorized', status_code=401)

        return await call_next(request)