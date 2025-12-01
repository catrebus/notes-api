from pydantic import BaseModel, EmailStr, Field


class RegistrationForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=3, max_length=255)
    email: EmailStr = Field(..., min_length=5, max_length=255)