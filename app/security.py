from fastapi import Security, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
from app.db.collections import users
from app.db.models import UserPublic

API_KEY_HEADER_NAME = "X-API-Key"
EMAIL_HEADER_NAME = "X-User-Email"

api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME)

async def get_current_user(
    api_key: str = Security(api_key_header),
    email: str = Header(..., alias=EMAIL_HEADER_NAME),
) -> UserPublic:
    doc = await users.find_one({"email": email, "api_key": api_key})
    if not doc:  
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    doc["containers"] = [container_name for container_name in doc.get("containers", [])]
    doc.pop("_id", None)
    return UserPublic(**doc)


