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
    """DTO for flexible food creation - supports both basic and comprehensive creation."""
    name: str = "Adana Kebap"
    description: Optional[str] = "Acılı kıyma kebabı, közde pişirilir"
    price: float = 45.0
    category: str = "Ana Yemek"
    recipes: List[RecipeWithTranslationsCreateDTO] = []
    translations: List[FoodTranslationCreateDTO] = []
    allergen_ids: List[int] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Adana Kebap",
                "description": "Acılı kıyma kebabı, közde pişirilir",
                "price": 45.0,
                "category": "Ana Yemek",
                "allergen_ids": [1, 2],
                "translations": [
                    {
                        "language_id": 1,
                        "name": "Adana Kebap",
                        "description": "Türkçe açıklama"
                    },
                    {
                        "language_id": 2,
                        "name": "Adana Kebab",
                        "description": "English description"
                    }
                ],
                "recipes": [
                    {
                        "ingredient_name": "Kıyma",
                        "quantity": "500g",
                        "step_order": 1,
                        "instruction": "Kıymayı baharatlarla karıştır",
                        "allergen_ids": [],
                        "translations": [
                            {
                                "language_id": 2,
                                "ingredient_name": "Minced Meat",
                                "instruction": "Mix meat with spices"
                            }
                        ]
                    }
                ]
            }
        }


class AllergenOutDTO(BaseModel):
    """DTO for allergen response data."""
    id: int
    code: str
    icon: Optional[str] = None
    
    class Config:
        from_attributes = True

class RecipeOutWithTranslationsDTO(BaseModel):
    """DTO for recipe with translations and allergens."""
    id: int
    ingredient_name: str
    quantity: str
    step_order: int
    instruction: Optional[str] = None
    allergens: List[AllergenOutDTO] = []
    translations: List['RecipeTranslationOutDTO'] = []
    
    class Config:
        from_attributes = True

class RecipeTranslationOutDTO(BaseModel):
    """DTO for recipe translation response."""
    id: int
    language_id: int
    ingredient_name: str
    instruction: Optional[str] = None
    
    class Config:
        from_attributes = True

class FoodTranslationOutDTO(BaseModel):
    """DTO for food translation response."""
    id: int
    language_id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class FoodOutDTO(BaseModel):
    """DTO for food response data."""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str
    dealer_id: int
    is_active: bool
    recipes: List[RecipeOutWithTranslationsDTO] = []
    allergens: List[AllergenOutDTO] = []
    translations: List[FoodTranslationOutDTO] = []
    
    class Config:
        from_attributes = True