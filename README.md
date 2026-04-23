# 📝 Simple Todo API with AI Descriptions

A modern REST API for managing todos with AI-powered automatic description generation.

---

## 🎯 Project Overview

**What it does:** A lightweight Todo management API that lets you create, read, update, and delete tasks. Unique feature: AI automatically generates task descriptions when you don't provide one.

**Use case:** Perfect for task management apps, learning REST APIs, or integrating AI into applications.

---

## 🏗️ Approach & Methodology

### Architecture
- **Framework:** FastAPI (modern, fast, auto-documented)
- **Language:** Python 3.11+
- **Storage:** In-memory (Python list)
- **AI Engine:** Google Gemini API (optional)
- **Validation:** Pydantic models (automatic request validation)

### Design Principles
1. **Simplicity First:** Minimal code, maximum functionality
2. **Optional AI:** Works without API key (graceful fallback)
3. **RESTful Design:** Proper HTTP methods and status codes
4. **Automatic Docs:** Built-in Swagger UI at `/docs`
5. **Type Safety:** Full type hints with Pydantic validation

### Data Structure
```python
class Todo:
    id: int                    # Auto-generated unique ID
    title: str                 # Task title (required)
    description: str           # Task description (auto-generated if empty)
    completed: bool            # Completion status (default: false)
    priority: str             # Priority level (low/medium/high)
    created_at: str           # ISO timestamp
```



## 📊 Data & Storage

**No external database required** - uses in-memory storage for simplicity.
- Data persists during server runtime
- Resets when server restarts
- Ideal for development and testing

To use a real database, replace `todos = []` with SQLAlchemy/MongoDB.

---

## 🚀 How to Run

### Option 1: Docker 
```bash
# Start API and all dependencies
docker-compose up

# API runs at http://localhost:8000
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Set up AI - create .env file:
echo "GEMINI_API_KEY=your_key_here" > .env

# 3. Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access at http://localhost:8000

## 📖 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API info |
| POST | `/todos` | Create todo (AI generates description if empty) |
| GET | `/todos` | Get all todos |
| GET | `/todos/{id}` | Get single todo |
| PUT | `/todos/{id}` | Update todo (partial update) |
| DELETE | `/todos/{id}` | Delete todo |
| POST | `/generate-description` | Generate AI description for any title |

---

## 📥 Sample Inputs & Outputs

### Create Todo (Auto AI Description)
**Request:**
```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker"}'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Learn Docker",
  "description": "Master Docker containerization for deploying applications efficiently",
  "completed": false,
  "priority": "medium",
  "created_at": "2026-04-22T18:14:28.241035"
}
```

### Create Todo (Custom Description)
**Request:**
```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review",
    "description": "Review pull requests on GitHub",
    "priority": "high"
  }'
```

**Response (200 OK):**
```json
{
  "id": 2,
  "title": "Code Review",
  "description": "Review pull requests on GitHub",
  "completed": false,
  "priority": "high",
  "created_at": "2026-04-22T18:15:30.123456"
}
```

### Get All Todos
**Request:**
```bash
curl http://localhost:8000/todos
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "description": "Master Docker containerization...",
    "completed": false,
    "priority": "medium",
    "created_at": "2026-04-22T18:14:28.241035"
  },
  {
    "id": 2,
    "title": "Code Review",
    "description": "Review pull requests on GitHub",
    "completed": false,
    "priority": "high",
    "created_at": "2026-04-22T18:15:30.123456"
  }
]
```

### Update Todo (Partial)
**Request:**
```bash
curl -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true, "priority": "low"}'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Learn Docker",
  "description": "Master Docker containerization...",
  "completed": true,
  "priority": "low",
  "created_at": "2026-04-22T18:14:28.241035"
}
```

### Generate AI Description
**Request:**
```bash
curl -X POST http://localhost:8000/generate-description \
  -H "Content-Type: application/json" \
  -d '{"title": "Deploy to production"}'
```

**Response (200 OK):**
```json
{
  "title": "Deploy to production",
  "generated_description": "Deploy application to production environment with proper monitoring and backup procedures"
}
```

### Delete Todo
**Request:**
```bash
curl -X DELETE http://localhost:8000/todos/2
```

**Response (200 OK):**
```json
{"message": "Todo deleted"}
```




## 🛠️ Tech Stack

- **FastAPI 0.104.1** - Modern web framework
- **Uvicorn 0.24.0** - ASGI server
- **Pydantic 2.5.0** - Data validation
- **Google Gemini API** - AI descriptions (optional)
- **Docker** - Containerization


### Using Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Create todo
response = requests.post(f"{BASE_URL}/todos", 
    json={"title": "Learn FastAPI"})
todo = response.json()

# Update todo
requests.put(f"{BASE_URL}/todos/{todo['id']}", 
    json={"completed": True})

# Get all
todos = requests.get(f"{BASE_URL}/todos").json()
print(f"Total: {len(todos)} todos")
```

### Using JavaScript/Node
```javascript
const BASE_URL = "http://localhost:8000";

// Create
const res = await fetch(`${BASE_URL}/todos`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "Learn FastAPI" })
});
const todo = await res.json();

// Update
await fetch(`${BASE_URL}/todos/${todo.id}`, {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ completed: true })
});
```



#### POST `/todos`
Create a new todo. **Description is auto-generated if not provided!**

**Request Body:**
```json
{
  "title": "Learn Python",
  "description": "Master Python programming basics",
  "completed": false
}
```

**Minimal Request (auto-generates description):**
```json
{
  "title": "Build a mobile app"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "title": "Build a mobile app",
  "description": "Create a mobile application that provides value to users. Focus on user experience and performance optimization for seamless functionality.",
  "completed": false,
  "created_at": "2024-01-15T12:00:00.123456",
  "updated_at": "2024-01-15T12:00:00.123456"
}
```

---

#### GET `/todos/{todo_id}`
Get a specific todo by ID.

**Example:**
```bash
curl http://localhost:8000/todos/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Study FastAPI fundamentals and build APIs with Python",
  "completed": false,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Todo with ID 999 not found",
  "status_code": 404
}
```

---

#### PUT `/todos/{todo_id}`
Update a todo. You can update any field (title, description, completed).

**Request Body (partial update):**
```json
{
  "completed": true
}
```

**Full Update Example:**
```json
{
  "title": "Advanced FastAPI",
  "description": "Learn advanced FastAPI concepts",
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Advanced FastAPI",
  "description": "Learn advanced FastAPI concepts",
  "completed": true,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T12:15:30.654321"
}
```

---

#### DELETE `/todos/{todo_id}`
Delete a todo by ID.

**Example:**
```bash
curl -X DELETE http://localhost:8000/todos/1
```

**Response (204 No Content):**
Empty response with status 204 indicating successful deletion.

---

### 🤖 AI Features

#### POST `/generate-description`
Generate an AI-powered description for any todo title.

**Request Body:**
```json
{
  "title": "Build a weather app"
}
```

**Response (200 OK):**
```json
{
  "title": "Build a weather app",
  "generated_description": "Create a weather application that fetches real-time weather data and displays it in a user-friendly interface with location-based services and forecast predictions."
}
```

**Use Cases:**
- Quick description generation for new todos
- Copy-paste generated descriptions into todo creation
- Ideation and brainstorming sessions
- Batch description generation

---

## 🎯 Usage Examples

### Example 1: Create a Todo with Auto-Generated Description

```bash
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Docker"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Learn Docker",
  "description": "Understand Docker containerization technology for packaging and deploying applications across different environments.",
  "completed": false,
  "created_at": "2024-01-15T10:30:00.123456",
  "updated_at": "2024-01-15T10:30:00.123456"
}
```

---

### Example 2: Create Multiple Todos

```bash
# Todo 1
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Setup database", "completed": false}'

# Todo 2
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Implement authentication", "completed": false}'

# Todo 3
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Write unit tests", "completed": false}'
```

---

### Example 3: Filter Incomplete Todos

```bash
curl "http://localhost:8000/todos?completed=false"
```

---

### Example 4: Update Todo Status to Complete

```bash
curl -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

---

### Example 5: Generate Description and Create Todo

```bash
# First, generate description
curl -X POST http://localhost:8000/generate-description \
  -H "Content-Type: application/json" \
  -d '{"title": "Optimize database queries"}'

# Then create todo with generated description
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Optimize database queries",
    "description": "Analyze and optimize database queries to improve application performance and reduce response times.",
    "completed": false
  }'
```

---


