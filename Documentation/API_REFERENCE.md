# API Reference & Examples

## Authentication Endpoints

### Register User
**Endpoint**: `POST /api/v1/auth/register`

**Request Body**:
```json
{
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "SecurePass123!"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "role": {
    "id": 1,
    "name": "user",
    "description": "Regular user",
    "created_at": "2024-01-20T10:00:00"
  },
  "created_at": "2024-01-20T10:00:00",
  "updated_at": "2024-01-20T10:00:00"
}
```

**Validations**:
- Email must be valid format
- Username: 3-100 alphanumeric characters (- and _ allowed)
- Password: minimum 8 characters
- Email and username must be unique

---

### Login User
**Endpoint**: `POST /api/v1/auth/login`

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "role": {
      "id": 1,
      "name": "user",
      "description": "Regular user",
      "created_at": "2024-01-20T10:00:00"
    },
    "created_at": "2024-01-20T10:00:00",
    "updated_at": "2024-01-20T10:00:00"
  }
}
```

**Error Responses**:
- 401 Unauthorized: Invalid email or password
- 403 Forbidden: Account is inactive

---

### Get Current User
**Endpoint**: `GET /api/v1/auth/me`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "role": { ... },
  "created_at": "2024-01-20T10:00:00",
  "updated_at": "2024-01-20T10:00:00"
}
```

---

## Task Endpoints

### Create Task
**Endpoint**: `POST /api/v1/tasks`

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Complete project report",
  "description": "Finish Q1 quarterly report with metrics",
  "priority": "high"
}
```

**Response** (201 Created):
```json
{
  "id": 5,
  "title": "Complete project report",
  "description": "Finish Q1 quarterly report with metrics",
  "status": "pending",
  "priority": "high",
  "owner_id": 1,
  "is_completed": false,
  "created_at": "2024-01-20T10:30:00",
  "updated_at": "2024-01-20T10:30:00"
}
```

**Validations**:
- Title: required, 1-255 characters
- Description: optional, max 1000 characters
- Priority: low, medium, or high (default: medium)

---

### Get User's Tasks
**Endpoint**: `GET /api/v1/tasks?skip=0&limit=10`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Query Parameters**:
- `skip`: Number of tasks to skip (default: 0)
- `limit`: Maximum tasks to return (default: 10, max: 100)

**Response** (200 OK):
```json
{
  "total": 15,
  "tasks": [
    {
      "id": 5,
      "title": "Complete project report",
      "description": "Finish Q1 quarterly report",
      "status": "in_progress",
      "priority": "high",
      "owner_id": 1,
      "is_completed": false,
      "created_at": "2024-01-20T10:30:00",
      "updated_at": "2024-01-20T11:00:00"
    },
    {
      "id": 4,
      "title": "Review code changes",
      "description": null,
      "status": "pending",
      "priority": "medium",
      "owner_id": 1,
      "is_completed": false,
      "created_at": "2024-01-19T14:20:00",
      "updated_at": "2024-01-19T14:20:00"
    }
  ]
}
```

---

### Get Specific Task
**Endpoint**: `GET /api/v1/tasks/{task_id}`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Parameters**:
- `task_id`: ID of the task to retrieve

**Response** (200 OK):
```json
{
  "id": 5,
  "title": "Complete project report",
  "description": "Finish Q1 quarterly report",
  "status": "in_progress",
  "priority": "high",
  "owner_id": 1,
  "is_completed": false,
  "created_at": "2024-01-20T10:30:00",
  "updated_at": "2024-01-20T11:00:00"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Task not found"
}
```

---

### Update Task
**Endpoint**: `PUT /api/v1/tasks/{task_id}`

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body** (all fields optional):
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed",
  "priority": "low",
  "is_completed": true
}
```

**Response** (200 OK):
```json
{
  "id": 5,
  "title": "Updated task title",
  "description": "Updated description",
  "status": "completed",
  "priority": "low",
  "owner_id": 1,
  "is_completed": true,
  "created_at": "2024-01-20T10:30:00",
  "updated_at": "2024-01-20T12:00:00"
}
```

**Valid Status Values**: `pending`, `in_progress`, `completed`
**Valid Priority Values**: `low`, `medium`, `high`

---

### Delete Task
**Endpoint**: `DELETE /api/v1/tasks/{task_id}`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Parameters**:
- `task_id`: ID of the task to delete

**Response** (204 No Content):
No response body

**Error Response** (404 Not Found):
```json
{
  "detail": "Task not found"
}
```

---

## Health Check Endpoints

### Root Endpoint
**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Task Management API",
  "version": "1.0.0",
  "docs_url": "/docs",
  "status": "running"
}
```

### Health Check
**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Missing or invalid authorization header"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "Email or username already registered"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## JWT Token Structure

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:
```json
{
  "user_id": 1,
  "email": "john@example.com",
  "role": "user",
  "exp": 1705771200,
  "iat": 1705767600
}
```

**Token Lifetime**: 30 minutes (configurable)

---

## Complete Flow Examples

### Example 1: Create Task and Update It

```bash
# 1. Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dev@example.com",
    "username": "developer",
    "full_name": "Dev User",
    "password": "SecurePass123!"
  }'

# 2. Login (save token from response)
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dev@example.com",
    "password": "SecurePass123!"
  }'

# 3. Create task (replace TOKEN)
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "title": "Implement API",
    "description": "Build REST API with authentication",
    "priority": "high"
  }'

# 4. Update task (replace TASK_ID and TOKEN)
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "status": "in_progress"
  }'

# 5. Get all tasks
curl -X GET "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer TOKEN"

# 6. Delete task (replace TASK_ID)
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer TOKEN"
```

---

## Rate Limiting & Best Practices

1. **Token Expiration**: Tokens expire after 30 minutes - users must login again
2. **Error Handling**: Check response status codes
3. **Pagination**: Use skip/limit for large datasets
4. **Validation**: All input is validated server-side
5. **Security**: Always use HTTPS in production

---

## Postman Collection

Import this collection into Postman for easier testing:

```json
{
  "info": {
    "name": "Task Management API",
    "description": "Scalable REST API with JWT Auth"
  },
  "variable": [
    {
      "key": "BASE_URL",
      "value": "http://localhost:8000/api/v1",
      "type": "string"
    },
    {
      "key": "TOKEN",
      "value": "",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{BASE_URL}}/auth/register"
          }
        },
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "url": "{{BASE_URL}}/auth/login"
          }
        }
      ]
    },
    {
      "name": "Tasks",
      "item": [
        {
          "name": "Create Task",
          "request": {
            "method": "POST",
            "url": "{{BASE_URL}}/tasks"
          }
        },
        {
          "name": "Get Tasks",
          "request": {
            "method": "GET",
            "url": "{{BASE_URL}}/tasks"
          }
        }
      ]
    }
  ]
}
```
