"""
User-related Data Transfer Objects (DTOs) for API request/response handling.
"""

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    """DTO for user creation requests."""
    email: EmailStr
    password: str


class UserOutDTO(BaseModel):
    """DTO for user response data."""
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    """DTO for user login requests."""
    email: EmailStr
    password: str