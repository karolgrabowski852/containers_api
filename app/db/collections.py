from app.config import  settings
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.MONGODB_URL)

db = client[settings.MONGODB_DATABASE]

users = db["users"]
containers_db = db["containers"]
billing_records = db["billing_records"]
resources = db["resources"]
