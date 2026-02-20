# Architecture & Design Patterns

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │            React Single Page Application                 │    │
│  │  - Login/Register Components                             │    │
│  │  - Protected Routes with JWT                             │    │
│  │  - Task Management Dashboard                             │    │
│  │  - API Service Layer (Axios)                             │    │
│  │  - Local Storage for Token Management                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           ↓ HTTP/REST                            │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              FastAPI Framework                           │    │
│  │  ┌────────────────────────────────────────────────┐     │    │
│  │  │        HTTP Request → CORS Middleware         │     │    │
│  │  └────────────────────────────────────────────────┘     │    │
│  │                     ↓                                    │    │
│  │  ┌────────────────────────────────────────────────┐     │    │
│  │  │    JWT Authentication Middleware              │     │    │
│  │  │  - Extract & Validate Bearer Token            │     │    │
│  │  │  - Attach User Info to Request State          │     │    │
│  │  │  - Protect Routes (Skip Public Routes)        │     │    │
│  │  └────────────────────────────────────────────────┘     │    │
│  │                     ↓                                    │    │
│  │  ┌────────────────────────────────────────────────┐     │    │
│  │  │          Route Handlers (v1 API)              │     │    │
│  │  │  - /auth/register, /auth/login                │     │    │
│  │  │  - /tasks (CRUD)                              │     │    │
│  │  │  - Pydantic Request Validation                │     │    │
│  │  └────────────────────────────────────────────────┘     │    │
│  │                     ↓                                    │    │
│  │  ┌────────────────────────────────────────────────┐     │    │
│  │  │         Service Layer (Business Logic)        │     │    │
│  │  │  - AuthService (Register, Login, Validation)  │     │    │
│  │  │  - TaskService (CRUD Operations)              │     │    │
│  │  │  - Security Utils (JWT, Hashing)              │     │    │
│  │  │  - Input Sanitization & Validation            │     │    │
│  │  └────────────────────────────────────────────────┘     │    │
│  │                     ↓                                    │    │
│  │  ┌────────────────────────────────────────────────┐     │    │
│  │  │        Data Access Layer (ORM)                │     │    │
│  │  │  - SQLAlchemy Models                          │     │    │
│  │  │  - User, Task, Role Models                    │     │    │
│  │  │  - Database Session Management                │     │    │
│  │  └────────────────────────────────────────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           ↓ SQL                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              PostgreSQL Database                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │    │
│  │  │  Users   │  │  Roles   │  │  Tasks   │             │    │
│  │  │ Table    │  │ Table    │  │ Table    │             │    │
│  │  └──────────┘  └──────────┘  └──────────┘             │    │
│  │       ↓            ↑              ↓                     │    │
│  │     (FK)        (PK)            (FK)                    │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Layered Architecture (3-Tier)

### 1. Presentation Layer (Frontend)
- **Technology**: React 18
- **Responsibilities**:
  - User interface rendering
  - Form handling & validation
  - JWT token management
  - API communication via Axios
  - Routing & navigation
- **Key Components**:
  - Auth pages (Login, Register)
  - Dashboard with task management
  - Protected routes

### 2. Application Layer (Backend)
- **Technology**: FastAPI with Pydantic
- **Structural Layers**:

  **a) Controller/Route Layer**:
  - Handles HTTP requests
  - Validates request data with Pydantic schemas
  - Calls appropriate services
  - Returns JSON responses

  **b) Service Layer**:
  - Contains business logic
  - AuthService: authentication, token generation
  - TaskService: task CRUD operations
  - Security utilities: password hashing, JWT operations
  - Input sanitization & validation

  **c) Data Access Layer**:
  - SQLAlchemy ORM models
  - Database session management
  - Query building & execution
  - Transaction management

### 3. Data Layer (Database)
- **Technology**: PostgreSQL
- **Components**:
  - Users table (authentication)
  - Roles table (authorization)
  - Tasks table (business data)
  - Foreign key relationships

---

## Design Patterns Used

### 1. **MVC Pattern (Modified)**
```
Model (SQLAlchemy) → Controller (Routes) → View (JSON responses)
```
- Clear separation of concerns
- Each model has a corresponding route handler

### 2. **Service Layer Pattern**
```
Routes → Services → Data Access Layer
```
- Business logic separated from route handlers
- Reusable services across routes
- Easier testing and maintenance

### 3. **Dependency Injection**
```python
def get_tasks(db: Session = Depends(get_db)):
    # db is injected by FastAPI
    tasks = TaskService.get_user_tasks(db, user_id)
```
- Database session injected into routes
- Promotes loose coupling
- Enables testing with mock dependencies

### 4. **Schema Validation Pattern**
```python
class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: str

# FastAPI automatically validates incoming JSON
@app.post("/tasks")
async def create_task(task_data: TaskCreate):
    # task_data is validated
```
- Pydantic models for request/response validation
- Type safety
- Auto-generated documentation

### 5. **Middleware Pattern**
```
Request → CORS Middleware → JWT Middleware → Route Handler → Response
```
- JWT validation in middleware
- Cross-cutting concerns separated
- Reusable across all routes

### 6. **Security Pattern**
- **Password Security**: Bcrypt hashing with salt
- **Token Security**: JWT with HS256 algorithm
- **Input Security**: Validation & sanitization
- **SQL Security**: SQLAlchemy ORM prevents injection

### 7. **Repository Pattern (Partial)**
```python
# Services act as repositories
class TaskService:
    @staticmethod
    def create_task(db, task_data, user_id):
        # Data access abstraction
```

---

## Data Flow Examples

### Authentication Flow

```
1. User enters email & password
         ↓
2. Frontend sends POST /auth/login
         ↓
3. Backend Route validates input (Pydantic)
         ↓
4. AuthService.login_user() executes:
   - Query user by email
   - Verify password hash
   - Generate JWT token
         ↓
5. Return token + user info
         ↓
6. Frontend stores token in localStorage
         ↓
7. Future requests include: Authorization: Bearer <token>
```

### Task Creation Flow

```
1. User fills task form & submits
         ↓
2. Frontend sends POST /tasks with JWT token
         ↓
3. CORS Middleware allows request
         ↓
4. JWT Middleware validates token, extracts user_id
         ↓
5. Route handler receives request, validates schema
         ↓
6. TaskService.create_task() executes:
   - Sanitize input
   - Create Task object with owner_id
   - Commit to database
   - Return created task
         ↓
7. Frontend updates UI with new task
```

### Protected Route Flow

```
Request with Authorization header
         ↓
JWT Middleware:
  - Check for "Bearer <token>" format
  - Decode JWT
  - Verify signature & expiration
  - Attach user_id to request.state
         ↓
Route Handler:
  - Extract user_id from request.state
  - Ensure user owns the resource
  - Proceed with operation
         ↓
Response returned
```

---

## Security Architecture

### Authentication (Who are you?)
```
User credentials → Bcrypt Hash → Compare → JWT Token → Subsequent Requests
```

### Authorization (What can you do?)
```
JWT Token → Extract Role → Check Permissions → Allow/Deny Action
```

### Input Security
```
User Input → Pydantic Validation → Sanitization → Database Query
```

### Database Security
```
SQLAlchemy ORM → Prevent SQL Injection
Parameterized Queries → Safe execution
```

---

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
    ↓
Backend Instance 1
Backend Instance 2  ← Multiple stateless instances
Backend Instance 3
    ↓
PostgreSQL (Shared database)
```

### Database Scaling
- Connection pooling
- Read replicas for queries
- Sharding for large datasets
- Caching layer (Redis)

### Performance Optimization
- Database indexes on frequently queried columns
- Query optimization
- Pagination for large datasets
- Response caching

---

## Code Organization

### Separation of Concerns
```
routes/       → Handle HTTP requests
services/     → Business logic
models/       → Data models
schemas/      → Request/response validation
middleware/   → Cross-cutting concerns
utils/        → Reusable functions
database.py   → Database configuration
config.py     → Application configuration
```

### Module Dependencies
```
routes → services → models & utils
services → database
utils (no dependencies on above)
```

---

## Error Handling Strategy

### Hierarchy
```
FastAPI Exception Handler
         ↓
Service Layer (Business Logic Exceptions)
         ↓
Database Layer Exceptions
         ↓
Custom Error Responses (HTTP Status + JSON)
```

### Error Response Format
```json
{
  "detail": "User-friendly error message"
}
```

---

## Testing Architecture

```
Unit Tests:
  - Utils (security, validation, logger)
  - Services (business logic)

Integration Tests:
  - Routes with mocked database
  - Database operations

E2E Tests:
  - Full flow: Register → Login → CRUD
  - Frontend interactions
```

---

## Deployment Architecture

### Development
```
docker-compose up
  ├─ PostgreSQL on port 5432
  ├─ FastAPI on port 8000 (reload enabled)
  └─ React on port 3000 (hot reload)
```

### Production
```
Docker Images (Built once)
  ├─ Backend image
  ├─ Frontend image
  └─ PostgreSQL image
        ↓
Kubernetes/Docker Swarm
  ├─ Multiple Backend pods
  ├─ Frontend CDN
  └─ PostgreSQL with replication
        ↓
Load Balancer (Nginx)
  ├─ API requests → Backend
  └─ Static assets → CDN
```

---

## Database Schema Design

### Users Table
```
id (PK) → Auto-increment primary key
email (UNIQUE) → Unique email address
username (UNIQUE) → Unique username
hashed_password → Bcrypt hash (not plain password)
is_active → Account status
role_id (FK) → References roles table
created_at → Timestamp
updated_at → Timestamp
```

### Tasks Table
```
id (PK) → Auto-increment primary key
title → Task name
description → Optional details
status → ENUM: pending, in_progress, completed
priority → ENUM: low, medium, high
owner_id (FK) → References users table
is_completed → Boolean flag
created_at → Timestamp
updated_at → Timestamp
```

### Relationships
```
Users (1) ─── (M) Tasks
         └──> Role (M-to-1)

Each user has one role
Each user can have multiple tasks
Each task belongs to one user
```

---

## Configuration Management

### Environment-based Configuration
```python
# config.py uses BaseSettings from pydantic
# Reads from .env file or environment variables

# Development
DEBUG=True
LOG_LEVEL=DEBUG

# Production
DEBUG=False
LOG_LEVEL=ERROR
SECRET_KEY=<secure-random-key>
```

### Configuration Overrides
```
Environment Variables > .env File > Default Values
```

---

## Logging Architecture

### Log Levels
```
DEBUG:   Development details
INFO:    General information (login, task creation)
WARNING: Issues that might cause problems
ERROR:   Error occurred but system continues
CRITICAL: System failure
```

### Log Destinations
```
Console → stdout (development)
File → logs/ directory (production)
```

---

## Best Practices Implemented

✅ **DRY (Don't Repeat Yourself)**
- Reusable services
- Utility functions
- Base models

✅ **SOLID Principles**
- Single Responsibility: Each layer has one job
- Open/Closed: Extensible without modifying existing code
- Dependency Inversion: Depend on abstractions (services)

✅ **Clean Code**
- Descriptive names
- Proper formatting
- Comments where needed

✅ **Security**
- Passwords hashed
- Tokens validated
- Input sanitized
- SQL injection prevented

✅ **Performance**
- Database indexing
- Connection pooling
- Pagination
- Error handling

✅ **Maintainability**
- Clear structure
- Well-documented
- Easy to extend
- Modular design

---

For implementation details, see specific module documentations.
