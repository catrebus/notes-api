from starlette.requests import Request

from services.request_auth import AuthServiceProtocol


class APIKeyAuthService(AuthServiceProtocol):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def is_authorized(self, request: Request) -> bool:
        key = request.headers.get('API-KEY')
        return key == self._api_key
