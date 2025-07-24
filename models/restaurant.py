from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, JSON, Numeric
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, index=True)  # URL-friendly name
    description = Column(Text, nullable=True)
    
    # Contact Info
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Location
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    
    # Business Info
    cuisine_type = Column(String, nullable=True)  # Türk, İtalyan, vs.
    price_range = Column(Integer, default=2)  # 1=₺, 2=₺₺, 3=₺₺₺
    
    # Media
    logo_url = Column(String, nullable=True)
    cover_image_url = Column(String, nullable=True)
    
    # Operating Hours (JSON: {"monday": {"open": "09:00", "close": "22:00", "closed": false}})
    operating_hours = Column(JSON, nullable=True)
    
    # Features (JSON array: ["delivery", "takeaway", "credit_card", "reservations"])
    features = Column(JSON, default=[])
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="restaurants")
    foods = relationship("Food", back_populates="restaurant", cascade="all, delete-orphan")
    categories = relationship("RestaurantCategory", back_populates="restaurant", cascade="all, delete-orphan")
    settings = relationship("RestaurantSettings", back_populates="restaurant", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")


class RestaurantCategory(Base):
    __tablename__ = "restaurant_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)  # Kahvaltı, Ana Yemekler, vs.
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="categories")
    foods = relationship("Food", back_populates="category", cascade="all, delete-orphan")


class RestaurantSettings(Base):
    __tablename__ = "restaurant_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, unique=True)
    
    # Theme & Branding
    theme_color = Column(String, default="#667eea")
    secondary_color = Column(String, default="#764ba2")
    
    # Localization
    default_language = Column(String, default="tr")
    supported_languages = Column(JSON, default=["tr"])  # ["tr", "en", "ar"]
    currency = Column(String, default="TRY")
    
    # QR & Digital Menu
    qr_code_url = Column(String, nullable=True)
    menu_url = Column(String, nullable=True)  # Custom domain or subdomain
    
    # Business Settings
    tax_rate = Column(Float, default=0.20)  # %20 KDV
    service_fee = Column(Float, default=0.0)
    minimum_order = Column(Float, default=0.0)
    delivery_fee = Column(Float, default=0.0)
    delivery_time = Column(String, default="30-45 dk")  # Estimated delivery time
    
    # Notifications
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    push_notifications = Column(Boolean, default=True)
    
    # Features Toggle
    online_ordering = Column(Boolean, default=True)
    table_reservations = Column(Boolean, default=False)
    loyalty_program = Column(Boolean, default=False)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="settings")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    
    # Order Info
    order_number = Column(String, unique=True, index=True)  # ORD-20241201-001
    status = Column(String, default="pending")  # pending, confirmed, preparing, ready, delivered, cancelled
    order_type = Column(String, default="delivery")  # delivery, pickup, dine_in
    
    # Customer Info
    customer_name = Column(String, nullable=True)
    customer_phone = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    delivery_address = Column(Text, nullable=True)
    
    # Order Details
    items = Column(JSON, nullable=False)  # [{"food_id": 1, "quantity": 2, "price": 25.00, "notes": "Extra spicy"}]
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    delivery_fee = Column(Float, default=0.0)
    service_fee = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    # Payment
    payment_method = Column(String, nullable=True)  # cash, card, online
    payment_status = Column(String, default="pending")  # pending, paid, failed
    
    # Special Instructions
    notes = Column(Text, nullable=True)
    
    # Timestamps
    estimated_ready_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="orders")