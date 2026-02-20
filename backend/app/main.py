from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.config import settings
from app.database import engine, Base
from app.routes import v1_router
from app.models import User, Task, Role
from app.utils import get_logger
from app.middleware.auth_middleware import JWTAuthMiddleware
import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

logger = get_logger(__name__)

def wait_for_db(max_attempts=60, delay=2):
    attempts = 0
    while attempts < max_attempts:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            logger.info("✓ Database connection successful")
            time.sleep(2)
            Base.metadata.create_all(bind=engine)
            logger.info("✓ Database tables created/verified")
            return True
        except OperationalError as e:
            attempts += 1
            logger.warning(f"Database not ready ({attempts}/{max_attempts}), waiting... Error: {str(e)[:100]}")
            time.sleep(delay)
        except Exception as e:
            attempts += 1
            logger.warning(f"Error checking database ({attempts}/{max_attempts}): {str(e)[:100]}")
            time.sleep(delay)
    
    logger.error("Failed to connect to database after 60 attempts")
    raise Exception("Database initialization failed")

wait_for_db()

app = FastAPI(
    title=settings.APP_NAME,
    description="Scalable REST API with JWT Authentication and Role-Based Access Control",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(JWTAuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="A scalable REST API with JWT authentication and role-based access control",
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Include routes
app.include_router(v1_router)


@app.on_event("startup")
async def startup_event():
    """Initialize default values on startup"""
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Create default roles if they don't exist
        user_role = db.query(Role).filter(Role.name == "user").first()
        if not user_role:
            user_role = Role(name="user", description="Regular user")
            db.add(user_role)
        
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.add(admin_role)
        
        db.commit()
        logger.info("Default roles initialized")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        db.rollback()
    finally:
        db.close()


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API is up and running"""
    return {
        "message": "Task Management API",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "version": settings.APP_VERSION
    }


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
