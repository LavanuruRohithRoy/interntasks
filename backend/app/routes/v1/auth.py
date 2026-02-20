from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services import AuthService
from app.utils import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        409: {"description": "User already exists"},
        400: {"description": "Invalid input"}
    }
)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    responses={
        401: {"description": "Invalid credentials"},
        403: {"description": "Account is inactive"}
    }
)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login_user(db, login_data)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user info",
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "User not found"}
    }
)
async def get_current_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(lambda: None)
):
    return AuthService.get_user_by_id(db, user_id)
