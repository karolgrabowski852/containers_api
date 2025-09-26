from pydantic import BaseModel, Field
from datetime import datetime, UTC, timedelta
import secrets
from app.core.resources import resources

class User(BaseModel):
    email: str
    api_key: str = Field(default_factory=lambda: secrets.token_hex(32))
    global_bill: int = 0
    containers: list[str] = []


class UserPublic(BaseModel):
    email: str
    global_bill: int
    containers: list[str]

class ContainerSettings(BaseModel):
    owner_email: str
    cpu: float
    memory: float
    gpu: int


class Container(BaseModel):
    owner_email: str
    name: str
    image: str
    status: str
    last_billed: datetime = Field(default_factory=datetime.now(UTC))
    settings: ContainerSettings

    def get_billing_time(self, user: User) -> int:
        now = datetime.now(UTC)
        time_diff = now - self.last_billed
        total_time = int(time_diff.total_seconds())
        user.global_bill += float(
            self.settings.cpu * total_time * resources.cpu_cost +
            self.settings.memory * total_time * resources.memory_cost +
            self.settings.gpu * total_time * resources.gpu_cost
        )
        return total_time
