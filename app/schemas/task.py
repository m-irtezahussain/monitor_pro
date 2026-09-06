from pydantic import BaseModel, ConfigDict
from datetime import datetime

class GetTasksResponse(BaseModel):
    id: int
    name: str
    description: str | None
    deadline: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
