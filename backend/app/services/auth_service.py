from sqlalchemy.orm import Session
from app.models import User, Role
from app.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.utils import hash_password, verify_password, create_access_token, get_logger
from fastapi import HTTPException, status
from datetime import timedelta

logger = get_logger(__name__)


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> UserResponse:
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or username already registered"
            )
        
        role = db.query(Role).filter(Role.name == "user").first()
        if not role:
            role = Role(name="user", description="Regular user")
            db.add(role)
            db.commit()
            db.refresh(role)
        
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role_id=role.id,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"User registered successfully: {user_data.email}")
        return UserResponse.model_validate(new_user)
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> TokenResponse:
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            logger.warning(f"Failed login attempt for: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            logger.warning(f"Login attempt with inactive account: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        access_token_expires = timedelta(minutes=30)
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.name
        }
        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        
        logger.info(f"User logged in successfully: {login_data.email}")
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user)
        )
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserResponse:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.model_validate(user)
