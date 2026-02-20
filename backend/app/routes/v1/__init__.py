"""V1 Routes"""
from fastapi import APIRouter
from app.routes.v1.auth import router as auth_router
from app.routes.v1.tasks import router as tasks_router

# Combine all v1 routes
v1_router = APIRouter()
v1_router.include_router(auth_router)
v1_router.include_router(tasks_router)

__all__ = ["v1_router"]
