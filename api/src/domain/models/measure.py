from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Measure(BaseModel):
    measure_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    voltage: float
