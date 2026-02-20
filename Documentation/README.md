# Task Management API

Production-ready FastAPI backend with JWT auth + RBAC and a React frontend for task management.

## What You Get
- JWT auth (register, login)
- Role-based access (user/admin roles)
- Task CRUD with ownership rules
- PostgreSQL + SQLAlchemy ORM
- React UI with login, register, dashboard
- Docker Compose for full stack

## Quick Start (Docker)
```bash
cd interntask
docker-compose up --build
```

## URLs
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure (High Level)
```
interntask/
├── backend/   # FastAPI app
├── frontend/  # React app
├── docker-compose.yml
└── Documentation/
```

## Environment
Backend uses:
- DATABASE_URL
- SECRET_KEY

Frontend uses:
- REACT_APP_API_URL

See [Documentation/SETUP.md](Documentation/SETUP.md) for details.
See [Documentation/API_REFERENCE.md](Documentation/API_REFERENCE.md) for endpoints.# Task Management API - Scalable REST API with Auth & RBAC

A production-ready, scalable REST API built with Python FastAPI featuring JWT authentication, role-based access control (RBAC), and a modern React frontend for task management.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend Layer (React)                       │
│  Login → Register → Dashboard → CRUD Tasks → Logout              │
│              (JWT Token Storage)                                 │
└──────────────────────────────────┬──────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │ HTTP REST API (FastAPI)     │
                    └──────────────┬──────────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────┐
│                     Backend Layer                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ JWT Middleware → Route Handler → Service Layer         │   │
│  │ ↓ Validation → ↓ Business Logic → ↓ DB Operations      │   │
│  └─────────────────────────────────────────────────────────┘   │
│  - Authentication (Register/Login)                              │
│  - Authorization (RBAC)                                         │
│  - CRUD Operations on Tasks                                     │
│  - Input Validation & Sanitization                              │
│  - Error Handling & Logging                                     │
└──────────────────────────────────┬──────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │ PostgreSQL Database          │
                    │ - Users / Roles / Tasks      │
                    └──────────────────────────────┘
```

## Features

### Backend
- ✅ **User Management**: Registration, Login, Profile Management
- ✅ **Authentication**: JWT-based token generation and validation
- ✅ **Authorization**: Role-Based Access Control (RBAC)
- ✅ **CRUD APIs**: Create, Read, Update, Delete tasks
- ✅ **API Versioning**: `/api/v1/` endpoint structure
- ✅ **Input Validation**: Pydantic schemas with comprehensive validation
- ✅ **Error Handling**: Centralized error responses with proper HTTP status codes
- ✅ **Logging**: Structured logging for debugging and monitoring
- ✅ **Database**: PostgreSQL with SQLAlchemy ORM
- ✅ **API Documentation**: Auto-generated Swagger/OpenAPI documentation

### Frontend
- ✅ **Authentication Pages**: Responsive Login & Register forms
- ✅ **Protected Routes**: JWT token-based access control
- ✅ **Dashboard**: Task overview with statistics
- ✅ **Task Management**: Create, Edit, Delete, Filter tasks
- ✅ **Status Tracking**: Mark tasks as pending, in-progress, or completed
- ✅ **Priority Levels**: Low, Medium, High priority indicators
- ✅ **Responsive Design**: Mobile-friendly UI

## Project Structure

```
interntask/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Configuration management
│   │   ├── database.py             # Database setup & session
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── role.py
│   │   ├── schemas/                # Pydantic validation schemas
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── services/               # Business logic
│   │   │   ├── auth_service.py
│   │   │   └── task_service.py
│   │   ├── routes/                 # API endpoints
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       └── tasks.py
│   │   ├── middleware/             # Custom middleware
│   │   │   └── auth_middleware.py
│   │   └── utils/                  # Utilities
│   │       ├── security.py         # Password hashing, JWT
│   │       ├── validators.py       # Input validation
│   │       └── logger.py           # Logging setup
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variables template
│   ├── Dockerfile                  # Docker image configuration
│   └── init_db.py                  # Database initialization script
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── components/
│   │   │   ├── TaskForm.jsx
│   │   │   ├── TaskList.jsx
│   │   │   ├── TaskItem.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── [CSS files]
│   │   ├── services/
│   │   │   └── api.js              # Axios API client
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
│
├── docker-compose.yml              # Docker orchestration
└── README.md                        # This file
```

## Quick Start

### Prerequisites
- Docker & Docker Compose (or)
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (if not using Docker)

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone and navigate to project
cd interntask

# Start all services
docker-compose up --build

# Services will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database URL

# Initialize database
python init_db.py

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start the development server
npm start
```

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register   - Register new user
POST   /api/v1/auth/login      - Login user (returns JWT token)
GET    /api/v1/auth/me         - Get current user info
```

### Tasks
```
GET    /api/v1/tasks           - Get all tasks (with pagination)
POST   /api/v1/tasks           - Create new task
GET    /api/v1/tasks/{id}      - Get specific task
PUT    /api/v1/tasks/{id}      - Update task
DELETE /api/v1/tasks/{id}      - Delete task
```

### Health Check
```
GET    /                        - Root endpoint
GET    /health                  - Health check
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication Flow

1. **Register**: `/api/v1/auth/register` - Create account with email/username/password
2. **Login**: `/api/v1/auth/login` - Receive JWT access token
3. **Store Token**: Frontend stores JWT in localStorage
4. **Include Token**: Add `Authorization: Bearer <token>` header to protected requests
5. **Validate Token**: Backend validates JWT in middleware for protected routes
6. **Logout**: Clear token from localStorage

## Sample Requests

### Register User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Create Task (requires token)
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{
    "title": "Complete project report",
    "description": "Finish Q1 project report",
    "priority": "high"
  }'
```

### Get Tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?skip=0&limit=10" \
  -H "Authorization: Bearer <your_jwt_token>"
```

## Database Schema

### Users Table
```sql
- id (Primary Key)
- email (Unique)
- username (Unique)
- full_name
- hashed_password
- is_active
- role_id (Foreign Key)
- created_at
- updated_at
```

### Tasks Table
```sql
- id (Primary Key)
- title
- description
- status (pending, in_progress, completed)
- priority (low, medium, high)
- owner_id (Foreign Key → Users)
- is_completed
- created_at
- updated_at
```

### Roles Table
```sql
- id (Primary Key)
- name (user, admin)
- description
- created_at
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Security Features

- ✅ **Password Hashing**: Bcrypt hashing with salt
- ✅ **JWT Tokens**: Secure token-based authentication
- ✅ **Input Validation**: Pydantic for request validation
- ✅ **Input Sanitization**: String cleaning to prevent XSS
- ✅ **CORS**: Configured for secure cross-origin requests
- ✅ **Error Messages**: Generic error messages to prevent information leakage
- ✅ **Token Expiration**: Configurable JWT expiration time
- ✅ **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

## Scaling Considerations

### Horizontal Scaling
- Stateless API design allows multiple backend instances
- Use load balancer (Nginx, HAProxy) to distribute requests
- Database connection pooling for efficient resource usage

### Caching
- Redis can be added for token blacklist/sessions
- Task caching for frequently accessed data
- Consider CDN for frontend static assets

### Monitoring & Logging
- Structured logging for analysis and debugging
- Application metrics and health checks
- Error tracking and alerting

### Database
- PostgreSQL indexes on frequently queried columns
- Regular backups and replication
- Consider read replicas for scaling read operations

## Testing

```bash
# Run backend tests (when added)
cd backend
pytest

# Run frontend tests (when added)
cd frontend
npm test
```

## Deployment

### Docker Production Build
```bash
# Build images
docker-compose -f docker-compose.yml build

# Run in production
docker-compose up -d
```

### Environment-Specific Configs
- Use `.env` files for different environments
- Update `SECRET_KEY` for production
- Enable HTTPS/TLS
- Configure proper logging and monitoring

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database credentials

### JWT Token Expired
- Token expires after 30 minutes (configurable)
- User needs to log in again to get new token

### CORS Errors
- Verify CORS_ORIGINS in backend .env
- Ensure frontend URL is in allowed origins

### Frontend API Connection
- Check REACT_APP_API_URL in frontend .env
- Ensure backend is running on correct port
- Open browser console for detailed error messages

## Future Enhancements

- [ ] Email verification for new users
- [ ] Password reset functionality
- [ ] Task sharing and collaboration
- [ ] Notifications system
- [ ] File attachments for tasks
- [ ] Advanced search and filtering
- [ ] Task categories/labels
- [ ] Recurring tasks
- [ ] Task comments and activities log
- [ ] Dark mode UI

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT License - feel free to use this project for learning and development.

## Support

For issues, questions, or suggestions:
- Check documentation
- Review API docs at `/docs`
- Check error logs in backend console

---

**Created for Internship Task Submission**

A clean, scalable, production-ready REST API with authentication and role-based access control.
