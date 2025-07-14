"""
Recipe-related Data Transfer Objects (DTOs) for API request/response handling.
"""

from pydantic import BaseModel
from typing import Optional


class RecipeCreateDTO(BaseModel):
    """DTO for recipe creation requests."""
    ingredient_name: str
    quantity: str
    step_order: int
    instruction: Optional[str] = None


class RecipeOutDTO(BaseModel):
    """DTO for recipe response data."""
    id: int
    ingredient_name: str
    quantity: str
    step_order: int
    instruction: Optional[str] = None
    
    class Config:
        from_attributes = True