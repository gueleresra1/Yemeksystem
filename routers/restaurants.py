from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.restaurant import Restaurant, RestaurantCategory, RestaurantSettings, Order
from models.user import User
from auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Pydantic Models
class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    cuisine_type: Optional[str] = None
    price_range: int = 2

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    id: int
    slug: str
    owner_id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RestaurantCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    display_order: int = 0

class RestaurantCategoryResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: Optional[str] = None
    display_order: int
    is_active: bool

    class Config:
        from_attributes = True

class RestaurantSettingsUpdate(BaseModel):
    theme_color: Optional[str] = None
    secondary_color: Optional[str] = None
    default_language: Optional[str] = None
    supported_languages: Optional[List[str]] = None
    currency: Optional[str] = None
    tax_rate: Optional[float] = None
    service_fee: Optional[float] = None
    minimum_order: Optional[float] = None
    delivery_fee: Optional[float] = None
    delivery_time: Optional[str] = None

class OrderCreate(BaseModel):
    restaurant_id: int
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    delivery_address: Optional[str] = None
    items: List[dict]  # [{"food_id": 1, "quantity": 2, "price": 25.00}]
    order_type: str = "delivery"
    payment_method: Optional[str] = None
    notes: Optional[str] = None

# Utility functions
def generate_slug(name: str) -> str:
    """Generate URL-friendly slug from restaurant name"""
    import re
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', name.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    return f"{slug}-{uuid.uuid4().hex[:6]}"

def calculate_order_total(items: List[dict], tax_rate: float = 0.20, 
                         delivery_fee: float = 0.0, service_fee: float = 0.0) -> dict:
    """Calculate order totals"""
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount + delivery_fee + service_fee
    
    return {
        "subtotal": round(subtotal, 2),
        "tax_amount": round(tax_amount, 2),
        "delivery_fee": round(delivery_fee, 2),
        "service_fee": round(service_fee, 2),
        "total_amount": round(total, 2)
    }

# Restaurant endpoints
@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new restaurant"""
    # Generate unique slug
    slug = generate_slug(restaurant.name)
    
    # Create restaurant
    db_restaurant = Restaurant(
        **restaurant.dict(),
        slug=slug,
        owner_id=current_user.id
    )
    
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    
    # Create default settings
    default_settings = RestaurantSettings(restaurant_id=db_restaurant.id)
    db.add(default_settings)
    
    # Create default categories
    default_categories = [
        {"name": "Kahvaltı", "display_order": 1},
        {"name": "Ana Yemekler", "display_order": 2},
        {"name": "Tatlılar", "display_order": 3},
        {"name": "İçecekler", "display_order": 4},
    ]
    
    for cat_data in default_categories:
        category = RestaurantCategory(
            restaurant_id=db_restaurant.id,
            **cat_data
        )
        db.add(category)
    
    db.commit()
    
    return db_restaurant

@router.get("/", response_model=List[RestaurantResponse])
def get_restaurants(
    skip: int = 0,
    limit: int = 50,
    city: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """Get list of restaurants with filters"""
    query = db.query(Restaurant).filter(Restaurant.is_active == is_active)
    
    if city:
        query = query.filter(Restaurant.city.ilike(f"%{city}%"))
    
    if cuisine_type:
        query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%"))
    
    restaurants = query.offset(skip).limit(limit).all()
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Get restaurant by ID"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return restaurant

@router.get("/slug/{slug}", response_model=RestaurantResponse)
def get_restaurant_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get restaurant by slug"""
    restaurant = db.query(Restaurant).filter(Restaurant.slug == slug).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_update: RestaurantBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update restaurant (only owner can update)"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    # Check ownership
    if restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this restaurant"
        )
    
    # Update fields
    for field, value in restaurant_update.dict(exclude_unset=True).items():
        setattr(restaurant, field, value)
    
    restaurant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(restaurant)
    
    return restaurant

# Restaurant Categories
@router.post("/{restaurant_id}/categories", response_model=RestaurantCategoryResponse)
def create_restaurant_category(
    restaurant_id: int,
    category: RestaurantCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new category for restaurant"""
    # Verify restaurant ownership
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    db_category = RestaurantCategory(
        restaurant_id=restaurant_id,
        **category.dict()
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.get("/{restaurant_id}/categories", response_model=List[RestaurantCategoryResponse])
def get_restaurant_categories(restaurant_id: int, db: Session = Depends(get_db)):
    """Get categories for restaurant"""
    categories = db.query(RestaurantCategory).filter(
        RestaurantCategory.restaurant_id == restaurant_id,
        RestaurantCategory.is_active == True
    ).order_by(RestaurantCategory.display_order).all()
    
    return categories

# Restaurant Settings
@router.put("/{restaurant_id}/settings")
def update_restaurant_settings(
    restaurant_id: int,
    settings_update: RestaurantSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update restaurant settings"""
    # Verify ownership
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    settings = db.query(RestaurantSettings).filter(
        RestaurantSettings.restaurant_id == restaurant_id
    ).first()
    
    if not settings:
        settings = RestaurantSettings(restaurant_id=restaurant_id)
        db.add(settings)
    
    # Update fields
    for field, value in settings_update.dict(exclude_unset=True).items():
        setattr(settings, field, value)
    
    settings.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Settings updated successfully"}

# Orders
@router.post("/orders", response_model=dict)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create new order"""
    # Get restaurant settings for pricing
    settings = db.query(RestaurantSettings).filter(
        RestaurantSettings.restaurant_id == order.restaurant_id
    ).first()
    
    tax_rate = settings.tax_rate if settings else 0.20
    delivery_fee = settings.delivery_fee if settings else 0.0
    service_fee = settings.service_fee if settings else 0.0
    
    # Calculate totals
    totals = calculate_order_total(
        order.items, 
        tax_rate=tax_rate, 
        delivery_fee=delivery_fee, 
        service_fee=service_fee
    )
    
    # Generate order number
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    # Create order
    db_order = Order(
        restaurant_id=order.restaurant_id,
        order_number=order_number,
        order_type=order.order_type,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_email=order.customer_email,
        delivery_address=order.delivery_address,
        items=order.items,
        payment_method=order.payment_method,
        notes=order.notes,
        **totals
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return {
        "order_id": db_order.id,
        "order_number": db_order.order_number,
        "total_amount": db_order.total_amount,
        "status": db_order.status
    }

@router.get("/{restaurant_id}/orders")
def get_restaurant_orders(
    restaurant_id: int,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get orders for restaurant (owner only)"""
    # Verify ownership
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).limit(limit).all()
    
    return orders

@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify restaurant ownership
    restaurant = db.query(Restaurant).filter(Restaurant.id == order.restaurant_id).first()
    if not restaurant or restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    order.status = new_status
    order.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"Order status updated to {new_status}"}