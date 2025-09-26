from pydantic import BaseModel, Field
from app.config import settings, logger


class ResourcePool(BaseModel):
    id: int = Field(unique=True, default=1)
    cpu: float
    memory: float
    gpu: int

    async def save(self):
        from app.db.collections import resources
        await resources.update_one({"id": self.id}, {"$set": self.model_dump()}, upsert=True)

    @staticmethod
    async def get_resources():
        from app.db.collections import resources
        doc = await resources.find_one({"id": 1})
        if not doc:
            resources_obj = ResourcePool(
                cpu=settings.CPU,
                memory=settings.MEMORY,
                gpu=settings.GPU
            )
            await resources_obj.save()
            return resources_obj
        doc.pop("_id", None)
        return ResourcePool(**doc)

    async def create_container(
        self,
        owner_email: str,
        cpu: float,
        memory: float,
        gpu: int | None = None,
    ):

        from app.db.models import ContainerSettings
        if self.cpu < cpu or self.memory < memory:
            return None
        if gpu is not None and self.gpu < gpu:
            return None

        self.cpu -= cpu
        self.memory -= memory
        if gpu is not None:
            self.gpu -= gpu

        await self.save()
        logger.info(f"Created container for {owner_email} with CPU: {cpu}, Memory: {memory}, GPU: {gpu or 0}. Available resources - CPU: {self.cpu}, Memory: {self.memory}, GPU: {self.gpu}")


        return ContainerSettings(
            owner_email=owner_email,
            cpu=cpu,
            memory=memory,
            gpu=gpu or 0
        )
    

    async def delete_container(self, settings: 'ContainerSettings') -> None:

        self.cpu += settings.cpu
        self.memory += settings.memory
        self.gpu += settings.gpu
        logger.info(f"Deleted container with settis: {settings}. Available resources - CPU: {self.cpu}, Memory: {self.memory}, GPU: {self.gpu}")

