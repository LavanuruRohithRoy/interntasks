from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from fastapi import HTTPException, status
from app.utils import get_logger

logger = get_logger(__name__)


class TaskService:
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate, user_id: int) -> TaskResponse:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            owner_id=user_id,
            status="pending"
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        logger.info(f"Task created: {new_task.id} by user {user_id}")
        return TaskResponse.model_validate(new_task)
    
    @staticmethod
    def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[TaskResponse]:
        tasks = db.query(Task).filter(Task.owner_id == user_id).offset(skip).limit(limit).all()
        return [TaskResponse.model_validate(task) for task in tasks]
    
    @staticmethod
    def get_task(db: Session, task_id: int, user_id: int) -> TaskResponse:
        task = db.query(Task).filter(
            (Task.id == task_id) & (Task.owner_id == user_id)
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return TaskResponse.model_validate(task)
    
    @staticmethod
    def update_task(
        db: Session,
        task_id: int,
        task_data: TaskUpdate,
        user_id: int
    ) -> TaskResponse:
        task = db.query(Task).filter(
            (Task.id == task_id) & (Task.owner_id == user_id)
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        db.commit()
        db.refresh(task)
        
        logger.info(f"Task updated: {task_id} by user {user_id}")
        return TaskResponse.model_validate(task)
    
    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> bool:
        task = db.query(Task).filter(
            (Task.id == task_id) & (Task.owner_id == user_id)
        ).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        db.delete(task)
        db.commit()
        
        logger.info(f"Task deleted: {task_id} by user {user_id}")
        return True
    
    @staticmethod
    def get_task_count(db: Session, user_id: int) -> int:
        """Get total task count for a user"""
        return db.query(Task).filter(Task.owner_id == user_id).count()
