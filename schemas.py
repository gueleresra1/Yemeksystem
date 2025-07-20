from pydantic import BaseModel, EmailStr
# YENİ FOOD SCHEMA'LARI
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    pass  # TokenData artık boş, gerekirse silebilirsiniz




class RecipeCreate(BaseModel):
    ingredient_name: str
    quantity: str
    step_order: int
    instruction: Optional[str] = None

class RecipeOut(BaseModel):
    id: int
    ingredient_name: str
    quantity: str
    step_order: int
    instruction: Optional[str] = None
    
    class Config:
        from_attributes = True

class FoodCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    tags: Optional[List[str]] = []  # Etiketler listesi
    recipes: List[RecipeCreate]  # Reçete listesi

class FoodOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str
    tags: Optional[List[str]] = []  # Etiketler listesi
    dealer_id: int
    is_active: bool
    recipes: List[RecipeOut] = []
    
    class Config:
        from_attributes = True

        