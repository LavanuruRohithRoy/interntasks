# SETUP & RUNNING GUIDE

## Prerequisites Installation

### 1. Install Docker (Easiest Way)
- Download from: https://www.docker.com/products/docker-desktop
- Follow installation steps for your OS

### 2. OR Install Components Separately

**Python 3.11+**
- Download from: https://www.python.org/downloads/
- Add Python to PATH during installation

**Node.js 18+**
- Download from: https://nodejs.org/
- Choose LTS version

**PostgreSQL 15+**
- Download from: https://www.postgresql.org/download/
- Set superuser password during installation

---

## QUICK START (Docker Recommended)

### Step 1: Start Services
```bash
cd c:\Users\DELL\Rohith\interntask
docker-compose up --build
```

**Wait for all services to start:**
```
✓ postgres: ready
✓ backend: running on http://localhost:8000
✓ frontend: running on http://localhost:3000
```

### Step 2: Access the Application
- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 3: Test the Application
1. Click "Register" and create an account
2. Login with your credentials
3. Add tasks, mark them complete, delete them
4. Logout

---

## MANUAL SETUP (If Not Using Docker)

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env

# 6. Configure database in .env
# Edit .env file and set:
# DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb

# 7. Initialize database
python init_db.py
# You should see: ✓ Database initialization complete!

# 8. Run server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Server running at http://localhost:8000
```

### Frontend Setup (in new terminal)

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
copy .env.example .env

# 4. Start development server
npm start

# Frontend running at http://localhost:3000
```

### Database Setup (PostgreSQL)

If using PostgreSQL directly:

```sql
-- Connect to PostgreSQL as superuser
-- Create database user
CREATE USER taskuser WITH PASSWORD 'taskpass';

-- Create database
CREATE DATABASE taskdb OWNER taskuser;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;
```

---

## Testing the API

### Using Swagger UI (Easiest)
1. Go to: http://localhost:8000/docs
2. Click "Try it out" on endpoints
3. Test Register → Login → Create Task

### Using cURL

```bash
# 1. Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d {
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "SecurePass123!"
  }

# 2. Login (save the token!)
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d {
    "email": "test@example.com",
    "password": "SecurePass123!"
  }

# Copy the "access_token" from response

# 3. Create Task (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d {
    "title": "My First Task",
    "description": "Testing the API",
    "priority": "high"
  }

# 4. Get Tasks
curl -X GET "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer TOKEN"
```

---

## Common Issues & Solutions

### Port Already in Use
```bash
# Backend (8000)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (3000)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Database Connection Failed
- Ensure PostgreSQL is running
- Check credentials in .env match database
- Verify DATABASE_URL format

### "ModuleNotFoundError" in Backend
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "Cannot find module" in Frontend
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors
- Check CORS_ORIGINS in backend .env
- Ensure frontend URL is listed

---

## Stopping Services

### Docker
```bash
docker-compose down
# Remove containers and volumes:
docker-compose down -v
```

### Manual
- Stop backend: Ctrl+C in backend terminal
- Stop frontend: Ctrl+C in frontend terminal

---

## Project Features Summary

### Backend
✅ JWT Authentication
✅ Role-Based Access Control
✅ CRUD APIs
✅ Input Validation
✅ Error Handling
✅ Logging
✅ Auto API Documentation

### Frontend
✅ Login/Register Pages
✅ Protected Routes
✅ Task Dashboard
✅ CRUD Operations
✅ Real-time Status Updates
✅ Responsive Design

### Database
✅ PostgreSQL
✅ User Management
✅ Task Storage
✅ Role System

---

## Next Steps

1. **Explore API Documentation**: http://localhost:8000/docs
2. **Test All Endpoints**: Use Swagger UI
3. **Review Code**: Well-commented and structured
4. **Customize**: Add more models, endpoints, features
5. **Deploy**: Use Docker for production deployment

---

## Architecture Diagram

```
User Browser
    ↓ (HTTP)
React Frontend (Port 3000)
    ↓ (API Calls)
FastAPI Backend (Port 8000)
    ↓ (SQL)
PostgreSQL Database
```

---

For detailed documentation, see README.md

Happy coding! 🚀
