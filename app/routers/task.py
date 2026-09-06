from fastapi import APIRouter, HTTPException, status, Depends

from app.models.tasks import Tasks
from app.models.user import User

from app.services.dependencies import get_current_user
from app.schemas.task import GetTasksResponse, CreateTaskRequest, UpdateTaskRequest

router = APIRouter(
    prefix="/api/v1/task",
    tags=["Tasks"]
)

@router.get(
    "/get",
    response_model=list[GetTasksResponse],
)
async def get_tasks(user: User = Depends(get_current_user)):
    task = await user.tasks.all()
    return task

@router.post(
    "/create",
    response_model=list[GetTasksResponse]
)
async def create_task(data: CreateTaskRequest, user: User = Depends(get_current_user)):
    validation_check = await user.tasks.filter(
        name=data.name
    )

    if data.name in validation_check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task already exists."
        )
    
    try:
        await user.tasks.create(
            name=data.name,
            description=data.description,
            deadline=data.deadline
        )

        tasks = await user.tasks.all()

        return tasks

    except ValueError:
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="str(e)"
        )

@router.post(
    "/update/{id}",
    response_model=GetTasksResponse
)
async def update(id:int, data: UpdateTaskRequest, user: User = Depends(get_current_user)):
    task = await user.tasks.filter(
        id=id
    ).first()

    if None in task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task found related to this id."
        )
    
    try:
        task.name = data.name
        task.description = data.description
        task.deadline = data.deadline
        task.save

        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

