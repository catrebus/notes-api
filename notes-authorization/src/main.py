import uvicorn
from fastapi import FastAPI

from src.authorization_config import Config
from src.middleware import AuthMiddleware
from src.services import APIKeyAuthService

app = FastAPI()

# Подключение router


# Подключение middleware
app.add_middleware(AuthMiddleware, auth_service=APIKeyAuthService(Config.AUTHORIZATION_API_KEY))

if __name__ == "__main__":
    uvicorn.run(app, host=Config.AUTHORIZATION_API_HOST, port=Config.AUTHORIZATION_API_PORT)