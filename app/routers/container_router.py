from fastapi import APIRouter, Depends, HTTPException
from app.db.models import ContainerSettings, UserPublic, Container
from app.db.collections import users, containers_db
from app.core.security import get_current_user
from app.db.resources import ResourcePool

router = APIRouter(tags=["containers"])

@router.get("/containers/{name}", response_model=Container, status_code=200)
async def get_container(name: str, user: UserPublic = Depends(get_current_user)):
    container = await containers_db.find_one({"name": name, "owner_email": user.email})
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    return container

@router.post("/containers/", response_model=UserPublic, status_code=201)
async def create_container(
    name: str,
    image: str,
    cpu: float,
    memory: float,
    gpu: int,
    user: UserPublic = Depends(get_current_user)
):
    existing = await containers_db.find_one({"name": name, "owner_email": user.email})
    if existing:
        raise HTTPException(status_code=409, detail="Container name already exists for this user")
    resources = await ResourcePool.get_resources()
    settings = await resources.create_container(user.email, cpu, memory, gpu)
    if not settings:
        raise HTTPException(status_code=400, detail="Insufficient resources available")

    container = Container(
        owner_email=user.email,
        name=name,
        image=image,
        status="created",
        settings=settings
    )
    await containers_db.insert_one(container.model_dump())
    await users.update_one({"email": user.email}, {"$addToSet": {"containers": name}})

    doc = await users.find_one({"email": user.email})
    doc.pop("_id", None)
    return UserPublic(**doc)

@router.put("/containers/{name}/run", response_model=Container, status_code=200)
async def run_container(name: str, user: UserPublic = Depends(get_current_user)):
    container = await containers_db.find_one({"name": name, "owner_email": user.email})
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    if container["status"] == "running":
        raise HTTPException(status_code=400, detail="Container already running")
    await containers_db.update_one(
        {"name": name, "owner_email": user.email},
        {"$set": {"status": "running"}}
    )
    container["status"] = "running"
    container.pop("_id", None)  
    return Container(**container)

@router.put("/containers/{name}/stop", response_model=Container, status_code=200)
async def stop_container(name: str, user: UserPublic = Depends(get_current_user)):
    container = await containers_db.find_one({"name": name, "owner_email": user.email})
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    if container["status"] != "running":
        raise HTTPException(status_code=400, detail="Container is not running")
    await containers_db.update_one(
        {"name": name, "owner_email": user.email},
        {"$set": {"status": "stopped"}}
    )
    container["status"] = "stopped"
    container.pop("_id", None)  
    return Container(**container)

@router.delete("/containers/{name}", status_code=204)
async def delete_container(name: str, user: UserPublic = Depends(get_current_user)):
    container = await containers_db.find_one({"name": name, "owner_email": user.email})
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    resources = await ResourcePool.get_resources()
    await resources.delete_container(ContainerSettings(**container["settings"]))
    await containers_db.delete_one({"name": name, "owner_email": user.email})
    await users.update_one({"email": user.email}, {"$pull": {"containers": name}})
    return {"message": "Container deleted successfully"}