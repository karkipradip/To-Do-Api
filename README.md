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
- **AI Engine:** Google Gemini API 
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
```

### Option 3: Run Tests
```bash
python test_all_features.py
```

---

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

---


