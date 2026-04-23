"""
Simple Todo API with AI Description
A basic REST API for managing todos with AI-powered descriptions.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Simple Todo API with AI", version="1.0.0")

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# In-memory storage
todos = []
next_id = 1

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # Add priority field
    created_at: Optional[str] = None

class TodoUpdate(BaseModel):
    """Model for updating todo - all fields optional"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None

class AIDescriptionRequest(BaseModel):
    title: str

class AIDescriptionResponse(BaseModel):
    title: str
    generated_description: str

async def generate_ai_description(title: str) -> str:
    """Generate AI description using Gemini"""
    try:
        if not GEMINI_API_KEY:
            return f"Task: {title}. Add your description here."

        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Generate a concise description for a todo: '{title}'"
        response = model.generate_content(prompt)

        return response.text.strip() if response.text else f"Task: {title}"
    except:
        return f"Task: {title}. AI unavailable."

@app.get("/")
def root():
    return {"message": "Simple Todo API with AI", "version": "1.0.0"}

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    global next_id

    # Auto-generate description if not provided
    description = todo.description
    if not description:
        description = await generate_ai_description(todo.title)

    new_todo = Todo(
        id=next_id,
        title=todo.title,
        description=description,
        completed=todo.completed,
        priority=todo.priority,
        created_at=datetime.now().isoformat()
    )
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in todos:
        if todo.id == todo_id:
            # Update only provided fields
            if updated_todo.title is not None:
                todo.title = updated_todo.title
            if updated_todo.description is not None:
                todo.description = updated_todo.description
            if updated_todo.completed is not None:
                todo.completed = updated_todo.completed
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/generate-description", response_model=AIDescriptionResponse)
async def generate_description(request: AIDescriptionRequest):
    """Generate AI description for any title"""
    description = await generate_ai_description(request.title)
    return AIDescriptionResponse(
        title=request.title,
        generated_description=description
    )