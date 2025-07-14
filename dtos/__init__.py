"""
DTO (Data Transfer Object) package for Yemeksystem API.
Contains request/response schemas for data validation and serialization.
"""

from .user_dto import UserCreateDTO, UserOutDTO, UserLoginDTO
from .auth_dto import TokenDTO, TokenDataDTO
from .recipe_dto import RecipeCreateDTO, RecipeOutDTO
from .food_dto import FoodCreateDTO, FoodOutDTO
from .allergen_dto import (
    AllergenOutDTO, 
    AllergenCreateDTO, 
    AllergenUpdateDTO,
    AllergenListDTO,
    AllergenTranslationCreateDTO,
    AllergenTranslationUpdateDTO,
    AllergenTranslationDTO
)

__all__ = [
    # User DTOs
    "UserCreateDTO",
    "UserOutDTO", 
    "UserLoginDTO",
    # Auth DTOs
    "TokenDTO",
    "TokenDataDTO",
    # Recipe DTOs
    "RecipeCreateDTO",
    "RecipeOutDTO",
    # Food DTOs
    "FoodCreateDTO",
    "FoodOutDTO",
    # Allergen DTOs
    "AllergenOutDTO",
    "AllergenCreateDTO", 
    "AllergenUpdateDTO",
    "AllergenListDTO",
    "AllergenTranslationCreateDTO",
    "AllergenTranslationUpdateDTO",
    "AllergenTranslationDTO",
]