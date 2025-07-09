# API Routes Documentation

## Overview
This document describes the API routes available in the Yemeksystem application.

## Base URL
```
http://localhost:8000
```

## Authentication Routes
**Prefix:** `/auth`

### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

**Status Codes:**
- `200`: User successfully created
- `400`: Email already exists

### POST /auth/login
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200`: Login successful
- `401`: Invalid credentials

## User Routes
**Prefix:** `/users`

### GET /users/me
Get current user information (Protected route).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

**Status Codes:**
- `200`: User information retrieved
- `401`: Invalid or missing token

### GET /users/protected
Example protected route that requires authentication.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Hello user@example.com, this is a protected route!"
}
```

**Status Codes:**
- `200`: Access granted
- `401`: Invalid or missing token

## General Routes

### GET /
Simple greeting endpoint.

**Response:**
```json
"Hello Esra"
```

## Error Responses
All endpoints may return the following error format:

```json
{
  "detail": "Error message description"
}
```

## Authentication
Protected routes require JWT token in Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## File Structure
```
routers/
├── __init__.py
├── auth.py      # Authentication routes
└── users.py     # User management routes
```

## Adding New Routes
To add new routes:

1. Create a new router file in `routers/` directory
2. Import APIRouter and create router instance
3. Add your endpoints to the router
4. Include the router in `main.py`

**Example:**
```python
# routers/products.py
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def get_products():
    return {"products": []}
```

```python
# main.py
from routers import auth, users, products

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
```