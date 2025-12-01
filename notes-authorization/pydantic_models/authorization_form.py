from pydantic import BaseModel


class AuthorizationForm(BaseModel):
    username: str
    password: str