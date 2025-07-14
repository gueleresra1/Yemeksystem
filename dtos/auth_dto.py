"""
Authentication-related Data Transfer Objects (DTOs) for API request/response handling.
"""

from pydantic import BaseModel


class TokenDTO(BaseModel):
    """DTO for authentication token response."""
    access_token: str
    token_type: str


class TokenDataDTO(BaseModel):
    """DTO for token data validation."""
    pass  # TokenData artık boş, gerekirse silebilirsiniz