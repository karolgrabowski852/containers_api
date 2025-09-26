from pydantic import BaseModel
from app.config import settings

class ResourcePool(BaseModel):
    cpu: float
    memory: float
    gpu: int
    
    cpu_cost: float = 1 / 3600
    memory_cost: float = 0.5 / 3600
    gpu_cost: float = 5 / 3600


    @property
    def memory(self):
        return self.memory * 1024

    def create_container(self, owner_email: str, cpu: float, memory: float, gpu: float = None) -> bool:
        from app.db.models import ContainerSettings
        if self.cpu >= cpu and self.memory >= memory and (self.gpu >= gpu if gpu is not None else True):
            self.cpu -= cpu
            self.memory -= memory
            self.gpu -= gpu if gpu is not None else 0
            return ContainerSettings(
                owner_email=owner_email,
                cpu=cpu,
                memory=memory,
                gpu=gpu
                )
        return False
    
resources = ResourcePool(cpu=settings.CPU, memory=settings.MEMORY, gpu=settings.GPU)