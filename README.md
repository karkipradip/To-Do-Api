# Simple Todo API with AI Descriptions

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight REST API for managing todo items with an optional AI-assisted description generator. The project is built with FastAPI and supports standard CRUD operations, partial updates, and automatic description generation through Google Gemini when a description is not provided.

This project is a good fit for:

- learning FastAPI and REST API design
- building a simple backend for a task manager
- experimenting with optional AI features in a clean Python service

## Project Overview

The API allows users to:

- create todo items
- list all todos
- fetch a single todo by ID
- update selected fields of an existing todo
- delete a todo
- generate an AI description from a todo title


## Approach and Methodology

The project follows a simple API-first approach:

1. Define clear request and response models with Pydantic.
2. Expose RESTful endpoints with FastAPI.
3. Keep the storage layer minimal using a Python list for rapid development.
4. Make AI integration optional so the API still works without a Gemini API key.
5. Support partial updates for better client flexibility.



## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Google Generative AI (`google-generativeai`)
- Python Dotenv
- Docker and Docker Compose

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health/info route |
| `GET` | `/todos` | Return all todos |
| `GET` | `/todos/{todo_id}` | Return one todo by ID |
| `POST` | `/todos` | Create a new todo |
| `PUT` | `/todos/{todo_id}` | Partially update a todo |
| `DELETE` | `/todos/{todo_id}` | Delete a todo |
| `POST` | `/generate-description` | Generate an AI description from a title |

## How to Run the Project

### Option 1: Run Locally

#### 1. Clone the repository

```bash
git clone https://github.com/karkipradip/To-Do-Api.git
cd To-Do-Api
```

#### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

This step is optional. If you skip it, the API still works and uses a fallback description instead of AI-generated text.

#### 5. Start the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 6. Open the API

- API base URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Option 2: Run with Docker

```bash
docker-compose up --build
```

The API will be available at:

- `http://localhost:8000`

## Sample Inputs and Outputs

### 1. Create a Todo

#### Request

```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Finish FastAPI assignment\", \"priority\": \"high\"}"
```

#### Sample Response

```json
{
  "id": 1,
  "title": "Finish FastAPI assignment",
  "description": "Task: Finish FastAPI assignment. Add your description here.",
  "completed": false,
  "priority": "high",
  "created_at": "2026-04-23T15:30:00.123456"
}
```

If Gemini is configured, the `description` field may contain an AI-generated summary instead of the fallback text.

### 2. Get All Todos

#### Request

```bash
curl "http://localhost:8000/todos"
```

#### Sample Response

```json
[
  {
    "id": 1,
    "title": "Finish FastAPI assignment",
    "description": "Task: Finish FastAPI assignment. Add your description here.",
    "completed": false,
    "priority": "high",
    "created_at": "2026-04-23T15:30:00.123456"
  }
]
```

### 3. Update a Todo

#### Request

```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d "{\"completed\": true, \"priority\": \"medium\"}"
```

#### Sample Response

```json
{
  "id": 1,
  "title": "Finish FastAPI assignment",
  "description": "Task: Finish FastAPI assignment. Add your description here.",
  "completed": true,
  "priority": "medium",
  "created_at": "2026-04-23T15:30:00.123456"
}
```

### 4. Generate a Description Directly

#### Request

```bash
curl -X POST "http://localhost:8000/generate-description" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Prepare project presentation\"}"
```

#### Sample Response

```json
{
  "title": "Prepare project presentation",
  "generated_description": "Task: Prepare project presentation. Add your description here."
}
```

When Gemini is enabled, `generated_description` may return AI-written text instead.

### 5. Delete a Todo

#### Request

```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

#### Sample Response

```json
{
  "message": "Todo deleted"
}
```

## Example Request Body

```json
{
  "title": "Study API testing",
  "description": "Practice CRUD endpoint testing with Postman",
  "completed": false,
  "priority": "medium"
}
```

## Example Response Body

```json
{
  "id": 2,
  "title": "Study API testing",
  "description": "Practice CRUD endpoint testing with Postman",
  "completed": false,
  "priority": "medium",
  "created_at": "2026-04-23T15:42:10.654321"
}
`
