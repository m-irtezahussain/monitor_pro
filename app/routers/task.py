from fastapi import APIRouter, HTTPException, status, Depends

from app.models.tasks import Tasks
from app.models.user import User

from app.services.dependencies import get_current_user
from app.schemas.task import GetTasksResponse

router = APIRouter(
    prefix="/api/v1/task",
    tags=["Tasks"]
)

@router.get(
    "/get",
    response_model=GetTasksResponse,
)
async def get_tasks(user: User = Depends(get_current_user)):
    task = await user.tasks.all()
    return tasks