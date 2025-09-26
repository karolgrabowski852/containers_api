from fastapi import APIRouter, Depends, HTTPException
from app.db.models import User, UserPublic
from app.db.collections import users
from app.core.security import get_current_user

router = APIRouter()


@router.get("/users/", response_model=UserPublic)
async def get_user(user: UserPublic = Depends(get_current_user)):
    return user

@router.post("/users/", response_model=UserPublic, status_code=201)
async def create_user(email: str):
    existing_user = await users.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email)
    await users.insert_one(user.model_dump())
    return UserPublic(**user.model_dump())
