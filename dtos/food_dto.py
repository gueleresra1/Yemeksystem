"""
Food-related Data Transfer Objects (DTOs) for API request/response handling.
"""

from pydantic import BaseModel
from typing import List, Optional
from .recipe_dto import RecipeCreateDTO, RecipeOutDTO


class FoodCreateDTO(BaseModel):
    """DTO for food creation requests."""
    name: str
    description: Optional[str] = None
    price: float
    category: str
    recipes: List[RecipeCreateDTO]  # Reçete listesi


class FoodOutDTO(BaseModel):
    """DTO for food response data."""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str
    dealer_id: int
    is_active: bool
    recipes: List[RecipeOutDTO] = []
    
    class Config:
        from_attributes = True