from fastapi import APIRouter, Depends
import models
from dtos import UserOutDTO
import auth

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOutDTO)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.get("/protected")
def protected_route(current_user: models.User = Depends(auth.get_current_user)):
    return {"message": f"Hello {current_user.email}, this is a protected route!"}