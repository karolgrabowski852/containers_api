from fastapi import FastAPI
from app.routers import user_router
from app.core.resources import ResourcePool
from app.config import settings

resources = ResourcePool(cpu=settings.CPU, memory=settings.MEMORY, gpu=settings.GPU)
app = FastAPI()


app.include_router(user_router.router)

