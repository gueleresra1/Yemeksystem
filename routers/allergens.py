from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
from auth import get_current_user
from models import Allergen, AllergenTranslation, Language, User
from dtos.allergen_dto import (
    AllergenOutDTO, 
    AllergenCreateDTO, 
    AllergenUpdateDTO,
    AllergenListDTO,
    AllergenTranslationCreateDTO,
    AllergenTranslationUpdateDTO,
    AllergenTranslationDTO
)

router = APIRouter(prefix="/allergens", tags=["allergens"])

@router.get("/", response_model=AllergenListDTO)
async def get_allergens(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    language_code: Optional[str] = Query(None, description="Language code for translations (tr, en, de, fr)"),
    db: Session = Depends(get_db)
):
    """Get all allergens with pagination and optional language filter"""
    
    offset = (page - 1) * size
    
    query = db.query(Allergen).options(
        joinedload(Allergen.translations).joinedload(AllergenTranslation.language)
    )
    
    total = query.count()
    allergens = query.offset(offset).limit(size).all()
    
    # Convert to DTO format
    allergen_dtos = []
    for allergen in allergens:
        translations = []
        for trans in allergen.translations:
            if not language_code or trans.language.code == language_code:
                translations.append(AllergenTranslationDTO(
                    language_id=trans.language_id,
                    language_code=trans.language.code,
                    name=trans.name
                ))
        
        allergen_dtos.append(AllergenOutDTO(
            id=allergen.id,
            code=allergen.code,
            icon=allergen.icon,
            translations=translations,
            created_at=allergen.created_at,
            updated_at=allergen.updated_at
        ))
    
    return AllergenListDTO(
        allergens=allergen_dtos,
        total=total,
        page=page,
        size=size
    )

@router.get("/{allergen_id}", response_model=AllergenOutDTO)
async def get_allergen_by_id(
    allergen_id: int,
    db: Session = Depends(get_db)
):
    """Get specific allergen by ID with all translations"""
    
    allergen = db.query(Allergen).options(
        joinedload(Allergen.translations).joinedload(AllergenTranslation.language)
    ).filter(Allergen.id == allergen_id).first()
    
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    
    translations = []
    for trans in allergen.translations:
        translations.append(AllergenTranslationDTO(
            language_id=trans.language_id,
            language_code=trans.language.code,
            name=trans.name
        ))
    
    return AllergenOutDTO(
        id=allergen.id,
        code=allergen.code,
        icon=allergen.icon,
        translations=translations,
        created_at=allergen.created_at,
        updated_at=allergen.updated_at
    )

@router.post("/", response_model=AllergenOutDTO)
async def create_allergen(
    allergen_data: AllergenCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new allergen (Admin only)"""
    
    # Check if user is admin
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create allergens")
    
    # Check if code already exists
    existing = db.query(Allergen).filter(Allergen.code == allergen_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Allergen code already exists")
    
    # Create new allergen
    allergen = Allergen(
        code=allergen_data.code,
        icon=allergen_data.icon
    )
    
    db.add(allergen)
    db.commit()
    db.refresh(allergen)
    
    return AllergenOutDTO(
        id=allergen.id,
        code=allergen.code,
        icon=allergen.icon,
        translations=[],
        created_at=allergen.created_at,
        updated_at=allergen.updated_at
    )

@router.put("/{allergen_id}", response_model=AllergenOutDTO)
async def update_allergen(
    allergen_id: int,
    allergen_data: AllergenUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update allergen (Admin only)"""
    
    # Check if user is admin
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update allergens")
    
    allergen = db.query(Allergen).filter(Allergen.id == allergen_id).first()
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    
    # Update fields
    if allergen_data.code is not None:
        # Check if new code already exists
        existing = db.query(Allergen).filter(
            Allergen.code == allergen_data.code,
            Allergen.id != allergen_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Allergen code already exists")
        allergen.code = allergen_data.code
    
    if allergen_data.icon is not None:
        allergen.icon = allergen_data.icon
    
    db.commit()
    db.refresh(allergen)
    
    # Load translations
    allergen = db.query(Allergen).options(
        joinedload(Allergen.translations).joinedload(AllergenTranslation.language)
    ).filter(Allergen.id == allergen_id).first()
    
    translations = []
    for trans in allergen.translations:
        translations.append(AllergenTranslationDTO(
            language_id=trans.language_id,
            language_code=trans.language.code,
            name=trans.name
        ))
    
    return AllergenOutDTO(
        id=allergen.id,
        code=allergen.code,
        icon=allergen.icon,
        translations=translations,
        created_at=allergen.created_at,
        updated_at=allergen.updated_at
    )

@router.delete("/{allergen_id}")
async def delete_allergen(
    allergen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete allergen (Admin only)"""
    
    # Check if user is admin
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete allergens")
    
    allergen = db.query(Allergen).filter(Allergen.id == allergen_id).first()
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    
    db.delete(allergen)
    db.commit()
    
    return {"message": "Allergen deleted successfully"}

# Translation endpoint'leri - Login olan herkes yapabilir
@router.post("/{allergen_id}/translations", response_model=AllergenTranslationDTO)
async def create_allergen_translation(
    allergen_id: int,
    translation_data: AllergenTranslationCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Sadece login kontrolü
):
    """Create allergen translation (Any logged in user)"""
    
    # Check if allergen exists
    allergen = db.query(Allergen).filter(Allergen.id == allergen_id).first()
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    
    # Check if language exists
    language = db.query(Language).filter(Language.id == translation_data.language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    # Check if translation already exists
    existing = db.query(AllergenTranslation).filter(
        AllergenTranslation.allergen_id == allergen_id,
        AllergenTranslation.language_id == translation_data.language_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Translation already exists for this language")
    
    # Create translation
    translation = AllergenTranslation(
        allergen_id=allergen_id,
        language_id=translation_data.language_id,
        name=translation_data.name
    )
    
    db.add(translation)
    db.commit()
    db.refresh(translation)
    
    return AllergenTranslationDTO(
        language_id=translation.language_id,
        language_code=translation.language.code,
        name=translation.name
    )

@router.put("/{allergen_id}/translations/{language_id}", response_model=AllergenTranslationDTO)
async def update_allergen_translation(
    allergen_id: int,
    language_id: int,
    translation_data: AllergenTranslationUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Sadece login kontrolü
):
    """Update allergen translation (Any logged in user)"""
    
    translation = db.query(AllergenTranslation).options(
        joinedload(AllergenTranslation.language)
    ).filter(
        AllergenTranslation.allergen_id == allergen_id,
        AllergenTranslation.language_id == language_id
    ).first()
    
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    if translation_data.name is not None:
        translation.name = translation_data.name
    
    db.commit()
    db.refresh(translation)
    
    return AllergenTranslationDTO(
        language_id=translation.language_id,
        language_code=translation.language.code,
        name=translation.name
    )