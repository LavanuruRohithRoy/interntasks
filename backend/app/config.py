import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://taskuser:taskpass@postgres:5432/taskdb")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
APP_NAME = "Task Management API"
APP_VERSION = "1.0.0"
APP_ENV = "development"
DEBUG = True
LOG_LEVEL = "INFO"

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://frontend:3000",
]

class Settings:
    pass

settings = Settings()
settings.DATABASE_URL = DATABASE_URL
settings.SECRET_KEY = SECRET_KEY
settings.ALGORITHM = ALGORITHM
settings.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
settings.APP_NAME = APP_NAME
settings.APP_VERSION = APP_VERSION
settings.APP_ENV = APP_ENV
settings.DEBUG = DEBUG
settings.LOG_LEVEL = LOG_LEVEL
settings.CORS_ORIGINS = CORS_ORIGINS
