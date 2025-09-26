from fastapi import APIRouter, Depends, HTTPException
from app.db.models import User, UserPublic
from app.db.collections import users
from app.core.security import get_current_user
from app.db.resources import ResourcePool

router = APIRouter(tags=["users"])


@router.get("/users/", response_model=UserPublic, status_code=200)
async def get_user(user: UserPublic = Depends(get_current_user)):
    return user

@router.post("/users/", response_model=User, status_code=201)
async def create_user(email: str):
    existing_user = await users.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email)
    await users.insert_one(user.model_dump())
    return user 


@router.delete("/users/", status_code=204)
async def delete_user(user: UserPublic = Depends(get_current_user)):
    await users.delete_one({"email": user.email})
    return None


@router.get("/users/current_bill", response_model=float, status_code=200)
async def get_current_bill(user: UserPublic = Depends(get_current_user)):
    return await user.get_current_billing()


@router.put("/users/paycheck", response_model=float, status_code=200)
async def paycheck(user: UserPublic = Depends(get_current_user)):
    return await user.paycheck()

@router.get("/resources", response_model=dict, status_code=200)
async def get_resources(user: UserPublic = Depends(get_current_user)):
    resources = await ResourcePool.get_resources()
    return resources.model_dump()