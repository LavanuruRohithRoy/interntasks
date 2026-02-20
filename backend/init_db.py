"""Database initialization utility"""
import os
from sqlalchemy import create_engine, text
from app.database import Base, SessionLocal
from app.models import Role, User, Task
from app.config import settings

def init_db():
    """Initialize database and create tables"""
    # Create database tables
    Base.metadata.create_all(bind=SessionLocal().get_bind())
    print("✓ Database tables created successfully")
    
    # Create default roles
    db = SessionLocal()
    try:
        # Check if roles already exist
        user_role = db.query(Role).filter(Role.name == "user").first()
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        
        if not user_role:
            user_role = Role(name="user", description="Regular user with basic access")
            db.add(user_role)
            print("✓ Created 'user' role")
        
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator with full access")
            db.add(admin_role)
            print("✓ Created 'admin' role")
        
        db.commit()
        print("✓ Default roles initialized")
        
    except Exception as e:
        print(f"✗ Error creating roles: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("\n✓ Database initialization complete!")
