"""Task Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services import TaskService
from app.utils import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


def get_current_user_id(request: Request) -> int:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return user_id


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={400: {"description": "Invalid input"}}
)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return TaskService.create_task(db, task_data, user_id)


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Get user's tasks",
    responses={401: {"description": "Unauthorized"}}
)
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    tasks = TaskService.get_user_tasks(db, user_id, skip, limit)
    total = TaskService.get_task_count(db, user_id)
    return TaskListResponse(total=total, tasks=tasks)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"}
    }
)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return TaskService.get_task(db, task_id, user_id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"}
    }
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return TaskService.update_task(db, task_id, task_data, user_id)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"}
    }
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    TaskService.delete_task(db, task_id, user_id)
    return None
