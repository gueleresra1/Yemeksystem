"""
Food-related Data Transfer Objects (DTOs) for API request/response handling.
"""

from pydantic import BaseModel
from typing import List, Optional
from .recipe_dto import RecipeCreateDTO, RecipeOutDTO

class FoodTranslationCreateDTO(BaseModel):
    """DTO for food translation creation."""
    language_id: int
    name: str
    description: Optional[str] = None

class FoodTranslationDTO(BaseModel):
    """DTO for food translation response."""
    id: int
    language_id: int
    language_code: str
    name: str
    description: Optional[str] = None

class RecipeTranslationCreateDTO(BaseModel):
    """DTO for recipe translation creation."""
    language_id: int
    ingredient_name: str
    instruction: Optional[str] = None

class RecipeWithTranslationsCreateDTO(BaseModel):
    """DTO for recipe creation with translations and allergens."""
    ingredient_name: str
    quantity: str
    step_order: int
    instruction: Optional[str] = None
    translations: List[RecipeTranslationCreateDTO] = []
    allergen_ids: List[int] = []

class FoodCreateDTO(BaseModel):
    """DTO for basic food creation requests."""
    name: str
    description: Optional[str] = None
    price: float
    category: str
    recipes: List[RecipeCreateDTO]

class ComprehensiveFoodCreateDTO(BaseModel):
    """DTO for comprehensive food creation with translations, recipes, and allergens."""
    name: str
    description: Optional[str] = None
    price: float
    category: str
    translations: List[FoodTranslationCreateDTO] = []
    recipes: List[RecipeWithTranslationsCreateDTO] = []
    allergen_ids: List[int] = []

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