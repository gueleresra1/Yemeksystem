from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import User, Food, Recipe
from auth import get_current_user
import schemas

router = APIRouter(prefix="/foods", tags=["foods"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=schemas.FoodOut)
def create_food(
    food_data: schemas.FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Yemek oluştur - Sadece dealer'lar yapabilir"""
    
    # Sadece dealer'lar (role_id = 3) yemek ekleyebilir
    if current_user.role_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yemek eklemek için dealer yetkiniz olmalı"
        )
    
    # Yeni yemek oluştur
    new_food = Food(
        name=food_data.name,
        description=food_data.description,
        price=food_data.price,
        category=food_data.category,
        ingredients=food_data.ingredients,
        allergens=food_data.allergens,
        tags=food_data.tags,
        dealer_id=current_user.id,
        is_active=True
    )
    
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    
    # Reçeteleri ekle
    for recipe_data in food_data.recipes:
        recipe = Recipe(
            food_id=new_food.id,
            ingredient_name=recipe_data.ingredient_name,
            quantity=recipe_data.quantity,
            step_order=recipe_data.step_order,
            instruction=recipe_data.instruction
        )
        db.add(recipe)
    
    db.commit()
    db.refresh(new_food)
    
    return new_food

@router.get("/", response_model=List[schemas.FoodOut])
def get_foods(
    db: Session = Depends(get_db),
    category: str = None,
    dealer_id: int = None,
    active_only: bool = True
):
    """Tüm yemekleri listele (filtreleme ile)"""
    
    query = db.query(Food)
    
    if active_only:
        query = query.filter(Food.is_active == True)
    
    if category:
        query = query.filter(Food.category == category)
    
    if dealer_id:
        query = query.filter(Food.dealer_id == dealer_id)
    
    foods = query.all()
    return foods

@router.get("/{food_id}", response_model=schemas.FoodOut)
def get_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    """Tek yemek detayı (reçete dahil)"""
    
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yemek bulunamadı"
        )
    
    return food

@router.put("/{food_id}", response_model=schemas.FoodOut)
def update_food(
    food_id: int,
    food_data: schemas.FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Yemek güncelle - Sadece kendi yemeğini güncelleyebilir"""
    
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yemek bulunamadı"
        )
    
    # Sadece yemek sahibi veya admin güncelleyebilir
    if food.dealer_id != current_user.id and current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu yemeği güncelleme yetkiniz yok"
        )
    
    # Yemek bilgilerini güncelle
    food.name = food_data.name
    food.description = food_data.description
    food.price = food_data.price
    food.category = food_data.category
    food.ingredients = food_data.ingredients
    food.allergens = food_data.allergens
    food.tags = food_data.tags
    
    # Eski reçeteleri sil
    db.query(Recipe).filter(Recipe.food_id == food_id).delete()
    
    # Yeni reçeteleri ekle
    for recipe_data in food_data.recipes:
        recipe = Recipe(
            food_id=food.id,
            ingredient_name=recipe_data.ingredient_name,
            quantity=recipe_data.quantity,
            step_order=recipe_data.step_order,
            instruction=recipe_data.instruction
        )
        db.add(recipe)
    
    db.commit()
    db.refresh(food)
    
    return food

@router.delete("/{food_id}")
def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Yemek sil - Sadece kendi yemeğini silebilir"""
    
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Yemek bulunamadı"
        )
    
    # Sadece yemek sahibi veya admin silebilir
    if food.dealer_id != current_user.id and current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu yemeği silme yetkiniz yok"
        )
    
    # Soft delete - is_active = False
    food.is_active = False
    db.commit()
    
    return {"message": f"'{food.name}' başarıyla silindi"}

@router.get("/my/foods", response_model=List[schemas.FoodOut])
def get_my_foods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sadece kendi yemeklerimi getir"""
    
    # Sadece dealer'lar kendi yemeklerini görebilir
    if current_user.role_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu özellik sadece dealer'lar için"
        )
    
    foods = db.query(Food).filter(Food.dealer_id == current_user.id).all()
    return foods