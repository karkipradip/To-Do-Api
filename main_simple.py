"""
Simple Todo API
A basic REST API for managing todos.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Simple Todo API", version="1.0.0")

# In-memory storage
todos = []
next_id = 1

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None

@app.get("/")
def root():
    return {"message": "Simple Todo API", "version": "1.0.0"}

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
def create_todo(todo: Todo):
    global next_id
    new_todo = Todo(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=datetime.now().isoformat()
    )
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            updated = Todo(
                id=todo_id,
                title=updated_todo.title,
                description=updated_todo.description,
                completed=updated_todo.completed,
                created_at=todo.created_at
            )
            todos[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")