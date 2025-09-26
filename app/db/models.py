from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, UTC, timedelta
import secrets
from app.config import settings
from app.db.resources import ResourcePool
from typing import List



class UserPublic(BaseModel):
    email: str
    global_bill: int = 0
    containers: List[str] = []

    # Check how much user should be billed up to now
    async def get_current_billing(self) -> int:
        containers = await Container.find_many({"owner_email": self.email})
        return [await container.get_current_billing(self) for container in containers][-1] if containers else self.global_bill

    #"reset" the billing time after user has been billed and return the amount to be billed
    async def paycheck(self) -> None:
        containers = await Container.find_many({"owner_email": self.email})
        return [await container.paycheck(self) for container in containers][-1] if containers else self.global_bill


class User(UserPublic):
    api_key: str = Field(default_factory=lambda: secrets.token_hex(32))


class ContainerSettings(BaseModel):
    owner_email: EmailStr
    cpu: float
    memory: float
    gpu: int


class Container(BaseModel):
    owner_email: EmailStr
    name: str
    image: str
    status: str
    last_billed: datetime = Field(default_factory=lambda: datetime.now(UTC))
    settings: ContainerSettings

    async def get_current_billing(self, user: User) -> float:
        if self.status != "running":
            return user.global_bill
        now = datetime.now(UTC)
        time_diff = now - self.last_billed
        total_time = int(time_diff.total_seconds())
        
        user.global_bill += float(
            self.settings.cpu * total_time * settings.CPU_COST +
            self.settings.memory * total_time * settings.MEMORY_COST +
            self.settings.gpu * total_time * settings.GPU_COST
        )
        return user.global_bill

    async def paycheck(self, user: User) -> float:
        self.last_billed = datetime.now(UTC)
        return await self.get_current_billing(user)

    async def run(self) -> None:
        self.last_billed = datetime.now(UTC)
        self.status = "running"

    async def stop(self) -> None:
        await self.paycheck()
        self.status = "stopped"
