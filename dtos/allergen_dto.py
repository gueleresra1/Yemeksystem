from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class AllergenCreateDTO(BaseModel):
    code: str
    icon: Optional[str] = None

class AllergenUpdateDTO(BaseModel):
    code: Optional[str] = None
    icon: Optional[str] = None

class AllergenOutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    code: str
    icon: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class AllergenListDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    code: str
    icon: Optional[str] = None

class AllergenTranslationCreateDTO(BaseModel):
    allergen_id: int
    language_id: int
    name: str

class AllergenTranslationUpdateDTO(BaseModel):
    name: Optional[str] = None

class AllergenTranslationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    allergen_id: int
    language_id: int
    name: str
    created_at: datetime
    updated_at: datetime