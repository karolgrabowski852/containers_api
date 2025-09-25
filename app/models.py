from app.config import  settings
from motor.motor_asyncio import AsyncIOMotorClient
form pydantic import BaseModel, Field
from typing import Optional, List


client = AsyncIOMotorClient(settings.MONGODB_URL)

db = client[settings.MONGODB_DATABASE]
users = db.collection("users")
containers = db.collection("containers")
billing_records = db.collection("billing_records")


class User(BaseModel):
    email: str = Field(..., unique=True)
    API_key: str